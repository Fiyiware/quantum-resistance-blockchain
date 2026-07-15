"""Cadena de bloques QRB.

Mantiene la lista ordenada de bloques, el estado del mundo derivado
de aplicar todas las transacciones, y un mempool de transacciones
pendientes.

Persistencia en JSON dentro de un directorio de datos configurable.
"""

import time
from pathlib import Path

from qrb.block import Block
from qrb.crypto import is_valid_address
from qrb.state import WorldState
from qrb.storage import load_json, save_json
from qrb.transaction import Transaction

GENESIS_HASH = "0" * 64


class Chain:
    def __init__(self, data_dir: Path) -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.blocks_file = self.data_dir / "blocks.json"
        self.state_file = self.data_dir / "state.json"
        self.mempool_file = self.data_dir / "mempool.json"
        self.blocks: list[Block] = []
        self.state = WorldState()
        self.mempool: list[Transaction] = []
        self._load()

    def _load(self) -> None:
        if self.blocks_file.exists():
            self.blocks = [Block.from_dict(b) for b in load_json(self.blocks_file)]
        if self.state_file.exists():
            self.state = WorldState.from_dict(load_json(self.state_file))
        if self.mempool_file.exists():
            self.mempool = [
                Transaction.from_dict(t) for t in load_json(self.mempool_file)
            ]

    def _save(self) -> None:
        save_json(self.blocks_file, [b.to_dict() for b in self.blocks])
        save_json(self.state_file, self.state.to_dict())
        save_json(self.mempool_file, [t.to_dict() for t in self.mempool])

    def height(self) -> int:
        return len(self.blocks)

    def last_hash(self) -> str:
        if not self.blocks:
            return GENESIS_HASH
        return self.blocks[-1].hash()

    def init_genesis(self, founder_address: str, founder_supply: int) -> None:
        """Crea el bloque génesis y acredita el suministro inicial al fundador.

        El génesis es un caso especial: sin firma (no podría haberla,
        no hay un estado anterior) y sin transacciones.
        """
        if self.blocks:
            raise RuntimeError(
                "La cadena ya tiene génesis. Borra el directorio de datos para reiniciar."
            )
        self.state.credit(founder_address, founder_supply)
        genesis = Block(
            index=0,
            previous_hash=GENESIS_HASH,
            transactions=[],
            proposer_address=founder_address,
            timestamp=int(time.time()),
        )
        self.blocks.append(genesis)
        self._save()

    def add_to_mempool(self, tx: Transaction) -> None:
        """Añade una transacción al mempool tras validarla."""
        if not tx.is_valid():
            raise ValueError("Transacción inválida (firma no verifica)")
        if not is_valid_address(tx.recipient):
            raise ValueError(
                f"Dirección de destinatario inválida: {tx.recipient!r} "
                "(se espera '0x' + 40 caracteres hex)"
            )
        if tx.amount <= 0:
            raise ValueError("El monto debe ser positivo")
        # El nonce esperado tiene en cuenta otras transacciones de este
        # emisor que ya están pendientes en el mempool.
        pending_from_sender = sum(1 for m in self.mempool if m.sender == tx.sender)
        expected_nonce = self.state.nonce_of(tx.sender) + pending_from_sender
        if tx.nonce != expected_nonce:
            raise ValueError(
                f"Nonce incorrecto: esperaba {expected_nonce}, recibió {tx.nonce}"
            )
        # Comprobación de saldo teniendo en cuenta gastos pendientes.
        pending_spend = sum(m.amount for m in self.mempool if m.sender == tx.sender)
        if self.state.balance_of(tx.sender) < pending_spend + tx.amount:
            raise ValueError(f"Saldo insuficiente en {tx.sender} considerando mempool")
        self.mempool.append(tx)
        self._save()

    def propose_block(
        self,
        proposer_address: str,
        proposer_pubkey: bytes,
        proposer_privkey: bytes,
        max_txs: int = 100,
    ) -> Block:
        """Crea, firma y añade un bloque con transacciones del mempool."""
        txs = self.mempool[:max_txs]
        block = Block(
            index=self.height(),
            previous_hash=self.last_hash(),
            transactions=txs,
            proposer_address=proposer_address,
        )
        block.sign_with(proposer_pubkey, proposer_privkey)
        if not block.is_valid():
            raise RuntimeError("Bloque firmado pero no válido (bug interno)")
        # Aplicamos las transacciones al estado en orden.
        for tx in txs:
            self.state.apply_transaction(tx)
        self.blocks.append(block)
        self.mempool = self.mempool[max_txs:]
        self._save()
        return block

    def get_block(self, index: int) -> Block | None:
        if 0 <= index < len(self.blocks):
            return self.blocks[index]
        return None
