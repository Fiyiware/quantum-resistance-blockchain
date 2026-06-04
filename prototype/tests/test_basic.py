"""Tests básicos del prototipo QRB.

Ejecutar desde la carpeta prototype/:
    python -m tests.test_basic
o:
    python tests/test_basic.py
"""

import sys
import tempfile
from pathlib import Path

# Permite ejecutar como script suelto:
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from qrb.block import Block  # noqa: E402
from qrb.chain import Chain  # noqa: E402
from qrb.crypto import (  # noqa: E402
    address_from_pubkey,
    generate_keypair,
    is_valid_address,
    sign,
    verify,
)
from qrb.transaction import Transaction  # noqa: E402
from qrb.wallet import Wallet  # noqa: E402


def test_dilithium_sign_verify() -> None:
    pk, sk = generate_keypair()
    msg = b"hola QRB"
    sig = sign(msg, sk)
    assert verify(msg, sig, pk), "firma valida no verifica"
    assert not verify(b"otro mensaje", sig, pk), "firma alterada verifica (bug)"


def test_address_deterministic_and_format() -> None:
    pk, _ = generate_keypair()
    a1 = address_from_pubkey(pk)
    a2 = address_from_pubkey(pk)
    assert a1 == a2, "addresses no son deterministas"
    assert a1.startswith("0x"), f"address sin prefijo 0x: {a1}"
    assert len(a1) == 42, f"address con longitud incorrecta: {len(a1)} != 42"


def test_transaction_sign_verify_tamper() -> None:
    w = Wallet.create("alice")
    tx = Transaction(
        sender=w.address, recipient="0x" + "ab" * 20, amount=100, nonce=0
    )
    tx.sign_with(w.public_key, w.private_key)
    assert tx.is_valid(), "transaccion recien firmada no valida"

    # Alteramos el monto y la firma debe fallar.
    tx.amount = 200
    assert not tx.is_valid(), "transaccion alterada sigue siendo valida (bug)"


def test_end_to_end_chain_flow() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        data_dir = Path(tmp)
        wallets_dir = data_dir / "wallets"

        founder = Wallet.create("founder")
        founder.save(wallets_dir)
        alice = Wallet.create("alice")
        alice.save(wallets_dir)

        chain = Chain(data_dir)
        chain.init_genesis(founder.address, 1_000_000)

        # Balance inicial
        assert chain.state.balance_of(founder.address) == 1_000_000
        assert chain.state.balance_of(alice.address) == 0

        # Crear y enviar transacción
        tx = Transaction(
            sender=founder.address,
            recipient=alice.address,
            amount=500,
            nonce=0,
        )
        tx.sign_with(founder.public_key, founder.private_key)
        chain.add_to_mempool(tx)
        assert len(chain.mempool) == 1

        # Minar bloque
        block = chain.propose_block(
            founder.address, founder.public_key, founder.private_key
        )
        assert block.index == 1
        assert len(block.transactions) == 1
        assert block.is_valid()
        assert len(chain.mempool) == 0

        # Estado actualizado
        assert chain.state.balance_of(founder.address) == 999_500
        assert chain.state.balance_of(alice.address) == 500
        assert chain.state.nonce_of(founder.address) == 1
        assert chain.height() == 2  # genesis + 1 block


def test_double_spend_rejected() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        data_dir = Path(tmp)
        wallets_dir = data_dir / "wallets"
        founder = Wallet.create("founder")
        founder.save(wallets_dir)
        alice = Wallet.create("alice")
        alice.save(wallets_dir)

        chain = Chain(data_dir)
        chain.init_genesis(founder.address, 100)

        tx1 = Transaction(
            sender=founder.address, recipient=alice.address, amount=60, nonce=0
        )
        tx1.sign_with(founder.public_key, founder.private_key)
        chain.add_to_mempool(tx1)

        # Segunda tx por 60 (excede saldo restante 40)
        tx2 = Transaction(
            sender=founder.address, recipient=alice.address, amount=60, nonce=1
        )
        tx2.sign_with(founder.public_key, founder.private_key)
        try:
            chain.add_to_mempool(tx2)
            raise AssertionError("doble gasto no detectado")
        except ValueError:
            pass  # esperado


def test_block_proposer_pubkey_must_match_address() -> None:
    """Defensa contra suplantación del proposer: si la pubkey adjunta al
    bloque no corresponde a la proposer_address declarada, sign_with debe
    rechazar la firma e is_valid debe rechazar el bloque.

    Regresión correspondiente al fallo detectado en revisión externa
    (30 de mayo de 2026).
    """
    founder = Wallet.create("founder")
    impostor = Wallet.create("impostor")
    assert founder.address != impostor.address

    block = Block(
        index=1,
        previous_hash="0" * 64,
        transactions=[],
        proposer_address=founder.address,
    )

    # 1) sign_with debe rechazar la pubkey del impostor para una proposer_address de founder.
    try:
        block.sign_with(impostor.public_key, impostor.private_key)
        raise AssertionError("sign_with deberia rechazar pubkey ajena al proposer")
    except ValueError:
        pass  # esperado

    # 2) Inyectamos manualmente pubkey ajena + firma criptograficamente valida
    #    sobre el header. is_valid debe rechazar igualmente porque la
    #    correspondencia pubkey-address falla.
    block.proposer_pubkey = impostor.public_key
    block.proposer_signature = sign(block.header_payload(), impostor.private_key)
    assert not block.is_valid(), (
        "is_valid debe rechazar bloque con pubkey que no corresponde a proposer_address"
    )


def test_invalid_recipient_address_rejected() -> None:
    """Una transacción a una dirección de destinatario malformada debe
    rechazarse en el mempool, para evitar quemar fondos enviándolos a una
    dirección irrecuperable.

    Regresión correspondiente al bug detectado en pruebas manuales del CLI
    (2 de junio de 2026): se aceptaban destinatarios sin formato válido.
    """
    # is_valid_address: casos básicos
    assert is_valid_address("0x" + "ab" * 20), "direccion valida rechazada"
    assert not is_valid_address("no-soy-una-direccion"), "texto libre aceptado"
    assert not is_valid_address("0x123"), "direccion demasiado corta aceptada"
    assert not is_valid_address("0x" + "zz" * 20), "caracteres no-hex aceptados"
    assert not is_valid_address("ab" * 20), "direccion sin prefijo 0x aceptada"

    with tempfile.TemporaryDirectory() as tmp:
        data_dir = Path(tmp)
        wallets_dir = data_dir / "wallets"
        founder = Wallet.create("founder")
        founder.save(wallets_dir)

        chain = Chain(data_dir)
        chain.init_genesis(founder.address, 1_000)

        # add_to_mempool debe rechazar el destinatario inválido aunque la
        # firma sea criptográficamente válida.
        tx = Transaction(
            sender=founder.address,
            recipient="no-soy-una-direccion",
            amount=10,
            nonce=0,
        )
        tx.sign_with(founder.public_key, founder.private_key)
        try:
            chain.add_to_mempool(tx)
            raise AssertionError("destinatario invalido no detectado")
        except ValueError:
            pass  # esperado
        assert len(chain.mempool) == 0, "tx con destinatario invalido entro al mempool"


def run_all() -> None:
    tests = [
        test_dilithium_sign_verify,
        test_address_deterministic_and_format,
        test_transaction_sign_verify_tamper,
        test_end_to_end_chain_flow,
        test_double_spend_rejected,
        test_block_proposer_pubkey_must_match_address,
        test_invalid_recipient_address_rejected,
    ]
    for t in tests:
        print(f"  -> {t.__name__} ... ", end="", flush=True)
        t()
        print("OK")
    print(f"\nTodos los tests pasaron ({len(tests)}/{len(tests)})")


if __name__ == "__main__":
    print("Ejecutando tests del prototipo QRB:\n")
    run_all()

def test_load_json_corrupt_file_names_the_file():
    """load_json should raise ValueError with the file path on corrupt JSON."""
    from qrb.storage import load_json
    tmp = Path("test_corrupt.json")
    try:
        tmp.write_text("{bad: json}")
        try:
            load_json(tmp)
            raise AssertionError("ValueError not raised")
        except ValueError as exc:
            assert str(tmp) in str(exc), f"path {tmp} not in error: {exc}"
    finally:
        tmp.unlink(missing_ok=True)


def test_load_json_valid_file():
    """load_json should return parsed data on valid JSON."""
    from qrb.storage import load_json
    tmp = Path("test_valid.json")
    try:
        tmp.write_text('{"hello": "world"}')
        result = load_json(tmp)
        assert result == {"hello": "world"}
    finally:
        tmp.unlink(missing_ok=True)
