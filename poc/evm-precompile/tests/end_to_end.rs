//! End-to-end test: a real `revm` EVM transaction `CALL`s the `MLDSAVERIFY`
//! precompile at `0x101`, the ML-DSA-65 verification runs inside the EVM, and we
//! read back the 32-byte boolean word — exactly as a contract (or an EOA calling
//! the precompile directly) would.
//!
//! This is the step beyond the unit tests in `src/lib.rs`: there we called the
//! precompile through `Precompile::execute` directly; here the call goes through
//! the *whole* revm transaction pipeline (validation, intrinsic gas, the call
//! frame, the precompile provider dispatch, and result construction). It is the
//! closest thing to "running on a node" without forking Reth — which is the
//! funded Phase 1 work.
//!
//! The custom `PrecompileProvider` below is exactly how a Reth fork injects an
//! extra precompile: wrap the standard `EthPrecompiles`, claim one more address,
//! and dispatch it to our verifier.

use std::string::{String, ToString};

use fips204::ml_dsa_65;
use fips204::traits::{SerDes, Signer};
use qrb_evm_precompile_poc::{encode_input, MLDSA65_VERIFY, MLDSA65_VERIFY_ADDRESS};

use revm::context::{Cfg, Context, Evm, FrameStack, TxEnv};
use revm::context_interface::result::{ExecutionResult, Output};
use revm::context_interface::ContextTr;
use revm::database::InMemoryDB;
use revm::handler::instructions::EthInstructions;
use revm::handler::{precompile_output_to_interpreter_result, EthPrecompiles, PrecompileProvider};
use revm::interpreter::interpreter::EthInterpreter;
use revm::interpreter::{CallInputs, InterpreterResult};
use revm::primitives::{address, hardfork::SpecId, Address, AddressSet, Bytes, TxKind, U256};
use revm::state::AccountInfo;
use revm::{ExecuteEvm, MainContext};

/// The ML-DSA-65 verification precompile address (`MLDSA65_VERIFY_ADDRESS` = 0x101).
const MLDSA_ADDR: Address = address!("0000000000000000000000000000000000000101");

/// A precompile provider that augments the standard Ethereum set with the
/// `MLDSAVERIFY` precompile at `0x101`. This is the Reth-fork integration pattern.
#[derive(Debug)]
struct MlDsaPrecompiles {
    inner: EthPrecompiles,
    warm: AddressSet,
}

impl MlDsaPrecompiles {
    fn new(spec: SpecId) -> Self {
        let inner = EthPrecompiles::new(spec);
        let mut warm = AddressSet::default();
        warm.clone_from(inner.warm_addresses());
        warm.insert(MLDSA_ADDR);
        Self { inner, warm }
    }
}

impl<CTX> PrecompileProvider<CTX> for MlDsaPrecompiles
where
    CTX: ContextTr<Cfg: Cfg<Spec = SpecId>>,
{
    type Output = InterpreterResult;

    fn set_spec(&mut self, spec: <CTX::Cfg as Cfg>::Spec) -> bool {
        let changed = <EthPrecompiles as PrecompileProvider<CTX>>::set_spec(&mut self.inner, spec);
        self.warm.clone_from(self.inner.warm_addresses());
        self.warm.insert(MLDSA_ADDR);
        changed
    }

    fn run(
        &mut self,
        context: &mut CTX,
        inputs: &CallInputs,
    ) -> Result<Option<Self::Output>, String> {
        if inputs.bytecode_address == MLDSA_ADDR {
            let output = MLDSA65_VERIFY
                .execute(
                    &inputs.input.as_bytes(context),
                    inputs.gas_limit,
                    inputs.reservoir,
                )
                .map_err(|e| e.to_string())?;
            return Ok(Some(precompile_output_to_interpreter_result(
                output,
                inputs.gas_limit,
            )));
        }
        <EthPrecompiles as PrecompileProvider<CTX>>::run(&mut self.inner, context, inputs)
    }

    fn warm_addresses(&self) -> &AddressSet {
        &self.warm
    }
}

/// Send a single transaction that calls `0x101` with `data`, return its result.
fn call_mldsa_precompile(data: Vec<u8>) -> ExecutionResult {
    let caller = address!("0000000000000000000000000000000000000001");

    let mut db = InMemoryDB::default();
    db.insert_account_info(
        caller,
        AccountInfo {
            balance: U256::from(10).pow(U256::from(18)),
            ..Default::default()
        },
    );

    let spec = SpecId::default();
    let ctx = Context::mainnet().with_db(db);
    let mut evm = Evm {
        ctx,
        inspector: (),
        instruction: EthInstructions::<EthInterpreter, _>::new_mainnet_with_spec(spec),
        precompiles: MlDsaPrecompiles::new(spec),
        frame_stack: FrameStack::new_prealloc(8),
    };

    let tx = TxEnv::builder()
        .caller(caller)
        .kind(TxKind::Call(MLDSA_ADDR))
        .data(Bytes::from(data))
        .gas_limit(1_000_000)
        .build()
        .unwrap();

    evm.transact_one(tx).expect("handler returned an error")
}

/// Extract the returned call bytes from a successful execution.
fn success_output(result: ExecutionResult) -> Bytes {
    match result {
        ExecutionResult::Success {
            output: Output::Call(bytes),
            ..
        } => bytes,
        other => panic!("expected a successful call, got: {other:?}"),
    }
}

fn signed_fixture(message: &[u8]) -> ([u8; 1952], [u8; 3309]) {
    let (pk, sk) = ml_dsa_65::try_keygen().expect("keygen");
    let sig = sk.try_sign(message, b"").expect("sign");
    (pk.into_bytes(), sig)
}

#[test]
fn evm_call_to_precompile_returns_true_for_valid_signature() {
    // Sanity: the address constant in the lib matches the one used here.
    assert_eq!(MLDSA65_VERIFY_ADDRESS, 0x101);

    let message = b"QRB tx | to=0x8f5...26e amount=1000 nonce=0";
    let (pk, sig) = signed_fixture(message);
    let input = encode_input(&pk, &sig, message);

    let bytes = success_output(call_mldsa_precompile(input));
    assert_eq!(bytes.len(), 32, "precompile must return a 32-byte word");
    assert_eq!(
        bytes[31], 1,
        "a valid ML-DSA-65 signature must make the EVM call return true"
    );
}

#[test]
fn evm_call_to_precompile_returns_false_for_tampered_signature() {
    let message = b"QRB tx | to=0x8f5...26e amount=1000 nonce=0";
    let (pk, mut sig) = signed_fixture(message);
    sig[0] ^= 0xFF; // corrupt the signature

    let input = encode_input(&pk, &sig, message);
    let bytes = success_output(call_mldsa_precompile(input));
    assert_eq!(
        bytes[31], 0,
        "a tampered signature must make the EVM call return false"
    );
}
