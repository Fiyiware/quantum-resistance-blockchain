"""Estado del libro mayor: balances y nonces por cuenta."""

from dataclasses import dataclass, field

from qrb.crypto import is_valid_address
from qrb.transaction import Transaction


@dataclass
class AccountState:
    balance: int = 0
    nonce: int = 0


@dataclass
class WorldState:
    """Mapping address → AccountState. Es el 'estado del mundo'."""

    accounts: dict[str, AccountState] = field(default_factory=dict)

    def _ensure(self, address: str) -> AccountState:
        if address not in self.accounts:
            self.accounts[address] = AccountState()
        return self.accounts[address]

    def balance_of(self, address: str) -> int:
        return self.accounts.get(address, AccountState()).balance

    def nonce_of(self, address: str) -> int:
        return self.accounts.get(address, AccountState()).nonce

    def credit(self, address: str, amount: int) -> None:
        if amount < 0:
            raise ValueError(f"no se puede acreditar un monto negativo: {amount}")
        self._ensure(address).balance += amount

    def debit(self, address: str, amount: int) -> None:
        acc = self._ensure(address)
        if acc.balance < amount:
            raise ValueError(f"Saldo insuficiente en {address}")
        acc.balance -= amount

    def increment_nonce(self, address: str) -> None:
        self._ensure(address).nonce += 1

    def apply_transaction(self, tx: Transaction) -> None:
        """Aplica una transacción ya validada al estado.

        Valida firma + nonce + saldo antes de mutar nada.
        """
        if not tx.is_valid():
            raise ValueError("Firma de transacción inválida")
        if not is_valid_address(tx.recipient):
            raise ValueError(f"dirección de destinatario inválida: {tx.recipient!r}")
        if tx.amount <= 0:
            raise ValueError(
                f"el monto debe ser estrictamente positivo, recibido {tx.amount}"
            )
        expected_nonce = self.nonce_of(tx.sender)
        if tx.nonce != expected_nonce:
            raise ValueError(
                f"Nonce incorrecto en tx: esperaba {expected_nonce}, "
                f"recibió {tx.nonce}"
            )
        if self.balance_of(tx.sender) < tx.amount:
            raise ValueError(f"Saldo insuficiente en {tx.sender}")
        self.debit(tx.sender, tx.amount)
        self.credit(tx.recipient, tx.amount)
        self.increment_nonce(tx.sender)

    def to_dict(self) -> dict:
        return {
            "accounts": {
                addr: {"balance": a.balance, "nonce": a.nonce}
                for addr, a in self.accounts.items()
            }
        }

    @classmethod
    def from_dict(cls, data: dict) -> "WorldState":
        ws = cls()
        for addr, a in data.get("accounts", {}).items():
            ws.accounts[addr] = AccountState(balance=a["balance"], nonce=a["nonce"])
        return ws
