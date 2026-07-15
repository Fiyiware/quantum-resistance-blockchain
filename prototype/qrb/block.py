"""Bloques QRB.

Cada bloque agrupa transacciones, incluye el hash del bloque anterior
(formando la cadena) y está firmado por el 'proposer' (en un L2 real,
el secuenciador; en este prototipo, cualquier wallet designada).
"""

import hashlib
import json
import time
from dataclasses import dataclass, field

from qrb.crypto import address_from_pubkey, sign, verify
from qrb.transaction import Transaction


@dataclass
class Block:
    index: int
    previous_hash: str
    transactions: list[Transaction]
    proposer_address: str
    proposer_pubkey: bytes = b""
    proposer_signature: bytes = b""
    timestamp: int = field(default_factory=lambda: int(time.time()))

    def tx_root(self) -> str:
        """Raíz simple de las transacciones (concatenación de hashes).

        En producción se usaría un Merkle tree para permitir pruebas
        de inclusión compactas.
        """
        if not self.transactions:
            return "0" * 64
        concatenated = "".join(tx.hash() for tx in self.transactions).encode()
        return hashlib.sha3_256(concatenated).hexdigest()

    def header_payload(self) -> bytes:
        """Bytes que se firman: cabecera del bloque + raíz de tx."""
        header = {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "tx_root": self.tx_root(),
            "proposer_address": self.proposer_address,
            "timestamp": self.timestamp,
        }
        return json.dumps(header, sort_keys=True, separators=(",", ":")).encode()

    def sign_with(self, public_key: bytes, private_key: bytes) -> None:
        """Firma el bloque tras verificar que la pubkey corresponde al proposer.

        Sin esta comprobación, un atacante podría declarar como proposer_address
        la dirección de cualquier víctima y firmar con su propia clave: el
        bloque se aceptaría porque la firma es válida respecto a la pubkey
        adjunta, sin reparar en que esa pubkey no es la del proposer
        declarado. Es la misma defensa que ya aplican las transacciones en
        Transaction.sign_with.
        """
        if address_from_pubkey(public_key) != self.proposer_address:
            raise ValueError(
                "La clave pública no corresponde a la dirección del proposer"
            )
        self.proposer_pubkey = public_key
        self.proposer_signature = sign(self.header_payload(), private_key)

    def hash(self) -> str:
        """Hash del bloque = SHA3-256(cabecera || firma del proposer)."""
        return hashlib.sha3_256(
            self.header_payload() + self.proposer_signature
        ).hexdigest()

    def is_valid(self, *, is_genesis: bool = False) -> bool:
        """Valida que la pubkey corresponde al proposer declarado, que la
        firma del bloque verifica con esa pubkey, y que cada transacción
        embarcada es a su vez válida.

        El bloque génesis es una excepción: no requiere firma (regla
        especial del protocolo).
        """
        if is_genesis:
            return self.index == 0 and len(self.transactions) == 0
        if not self.proposer_signature or not self.proposer_pubkey:
            return False
        # Defensa contra suplantación: la pubkey debe corresponder a la
        # dirección declarada del proposer. Sin esta comprobación, un
        # atacante podría falsificar la identidad del proposer.
        if address_from_pubkey(self.proposer_pubkey) != self.proposer_address:
            return False
        if not verify(
            self.header_payload(), self.proposer_signature, self.proposer_pubkey
        ):
            return False
        return all(tx.is_valid() for tx in self.transactions)

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "proposer_address": self.proposer_address,
            "proposer_pubkey": self.proposer_pubkey.hex(),
            "proposer_signature": self.proposer_signature.hex(),
            "tx_root": self.tx_root(),
            "transactions": [tx.to_dict() for tx in self.transactions],
            "hash": self.hash(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Block":
        return cls(
            index=data["index"],
            previous_hash=data["previous_hash"],
            transactions=[Transaction.from_dict(t) for t in data["transactions"]],
            proposer_address=data["proposer_address"],
            proposer_pubkey=bytes.fromhex(data["proposer_pubkey"]),
            proposer_signature=bytes.fromhex(data["proposer_signature"]),
            timestamp=data["timestamp"],
        )
