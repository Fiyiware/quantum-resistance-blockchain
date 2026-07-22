"""Transacciones QRB.

Modelo account-based (similar a Ethereum). Cada transacción mueve
una cantidad de QRB de una dirección emisora a una receptora, está
numerada por un 'nonce' que evita reenvíos, y va firmada con ML-DSA-65.

La transacción incluye la clave pública del emisor (necesaria para
verificar la firma, ya que la dirección por sí sola no la revela).
"""

import hashlib
import json
import time
from dataclasses import dataclass, field

from qrb.crypto import address_from_pubkey, sign, verify


@dataclass
class Transaction:
    sender: str
    recipient: str
    amount: int
    nonce: int
    timestamp: int = field(default_factory=lambda: int(time.time()))
    public_key: bytes = b""
    signature: bytes = b""

    def signing_payload(self) -> bytes:
        """Bytes que se firman: todos los campos salvo pubkey y firma.

        La serialización es JSON con claves ordenadas para que el
        resultado sea determinista entre máquinas.
        """
        payload = {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "nonce": self.nonce,
            "timestamp": self.timestamp,
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()

    def sign_with(self, public_key: bytes, private_key: bytes) -> None:
        """Firma la transacción y rellena los campos public_key / signature.

        Comprueba que la clave pública corresponde al sender declarado.
        """
        if address_from_pubkey(public_key) != self.sender:
            raise ValueError("La clave pública no corresponde a la dirección emisora")
        self.public_key = public_key
        self.signature = sign(self.signing_payload(), private_key)

    def is_valid(self) -> bool:
        """Comprueba firma + correspondencia pubkey↔sender."""
        if not self.signature or not self.public_key:
            return False
        if address_from_pubkey(self.public_key) != self.sender:
            return False
        return verify(self.signing_payload(), self.signature, self.public_key)

    def hash(self) -> str:
        """Hash SHA3-256 determinista de la transacción completa."""
        data = {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "nonce": self.nonce,
            "timestamp": self.timestamp,
            "public_key": self.public_key.hex(),
            "signature": self.signature.hex(),
        }
        serialized = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha3_256(serialized).hexdigest()

    def to_dict(self) -> dict:
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "nonce": self.nonce,
            "timestamp": self.timestamp,
            "public_key": self.public_key.hex(),
            "signature": self.signature.hex(),
            "hash": self.hash(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        return cls(
            sender=data["sender"],
            recipient=data["recipient"],
            amount=data["amount"],
            nonce=data["nonce"],
            timestamp=data["timestamp"],
            public_key=bytes.fromhex(data["public_key"]),
            signature=bytes.fromhex(data["signature"]),
        )
