#!/usr/bin/env python3
"""QRB CLI — interfaz de línea de comandos del prototipo.

Ejemplos de uso:

    python qrb_cli.py wallet create --name fundador
    python qrb_cli.py wallet create --name alice
    python qrb_cli.py wallet list
    python qrb_cli.py chain init --founder fundador --supply 1000000000
    python qrb_cli.py wallet balance --name fundador
    python qrb_cli.py tx send --from fundador --to 0x... --amount 1000
    python qrb_cli.py chain mine --proposer fundador
    python qrb_cli.py chain show
    python qrb_cli.py chain block --index 1
"""

import argparse
import json as _json
import sys
from pathlib import Path

from qrb.chain import Chain
from qrb.transaction import Transaction
from qrb.wallet import Wallet

DATA_DIR = Path(".qrb-data")
WALLETS_DIR = DATA_DIR / "wallets"


def cmd_wallet_create(args: argparse.Namespace) -> None:
    if (WALLETS_DIR / f"{args.name}.json").exists():
        print(f"ERROR: ya existe una wallet llamada '{args.name}'", file=sys.stderr)
        sys.exit(1)
    w = Wallet.create(args.name)
    path = w.save(WALLETS_DIR)
    print(f"OK Wallet '{args.name}' creada")
    print(f"   Direccion: {w.address}")
    print(f"   Archivo:   {path}")
    print(f"   Pubkey:    {len(w.public_key):,} bytes (ML-DSA-65)")
    print(f"   Privkey:   {len(w.private_key):,} bytes (ML-DSA-65)")


def cmd_wallet_list(args: argparse.Namespace) -> None:
    names = Wallet.list_all(WALLETS_DIR)
    if not names:
        print("(no hay wallets — crea una con: wallet create --name NOMBRE)")
        return
    print(f"{'NOMBRE':<20} DIRECCION")
    print("-" * 70)
    for name in names:
        w = Wallet.load(name, WALLETS_DIR)
        print(f"{name:<20} {w.address}")


def cmd_wallet_balance(args: argparse.Namespace) -> None:
    chain = Chain(DATA_DIR)
    if args.name:
        w = Wallet.load(args.name, WALLETS_DIR)
        addr = w.address
        label = args.name
    elif args.address:
        addr = args.address
        label = "(dirección externa)"
    else:
        print("Especifica --name o --address", file=sys.stderr)
        sys.exit(1)
    bal = chain.state.balance_of(addr)
    nonce = chain.state.nonce_of(addr)
    print(f"Wallet:    {label}")
    print(f"Direccion: {addr}")
    print(f"Saldo:     {bal:,} QRB")
    print(f"Nonce:     {nonce}")


def cmd_chain_init(args: argparse.Namespace) -> None:
    chain = Chain(DATA_DIR)
    if chain.blocks:
        print(
            "ERROR: la cadena ya tiene génesis. Borra .qrb-data/ para reiniciar.",
            file=sys.stderr,
        )
        sys.exit(1)
    w = Wallet.load(args.founder, WALLETS_DIR)
    chain.init_genesis(w.address, args.supply)
    print("OK Genesis creado")
    print(f"   Fundador:           {args.founder} ({w.address})")
    print(f"   Suministro inicial: {args.supply:,} QRB")
    print(f"   Hash genesis:       {chain.blocks[0].hash()}")


def cmd_tx_send(args: argparse.Namespace) -> None:
    sender_wallet = Wallet.load(args.sender, WALLETS_DIR)
    chain = Chain(DATA_DIR)
    pending = sum(1 for m in chain.mempool if m.sender == sender_wallet.address)
    nonce = chain.state.nonce_of(sender_wallet.address) + pending
    tx = Transaction(
        sender=sender_wallet.address,
        recipient=args.to,
        amount=args.amount,
        nonce=nonce,
    )
    tx.sign_with(sender_wallet.public_key, sender_wallet.private_key)
    chain.add_to_mempool(tx)
    print("OK Transaccion anadida al mempool")
    print(f"   Hash:   {tx.hash()}")
    print(f"   De:     {tx.sender}")
    print(f"   A:      {tx.recipient}")
    print(f"   Monto:  {tx.amount:,} QRB")
    print(f"   Nonce:  {tx.nonce}")
    print(f"   Firma:  {len(tx.signature):,} bytes (ML-DSA-65)")


def cmd_chain_mine(args: argparse.Namespace) -> None:
    chain = Chain(DATA_DIR)
    if not chain.mempool:
        print("(mempool vacío — no hay nada que minar)")
        return
    proposer = Wallet.load(args.proposer, WALLETS_DIR)
    block = chain.propose_block(
        proposer.address, proposer.public_key, proposer.private_key
    )
    print(f"OK Bloque #{block.index} minado")
    print(f"   Hash:           {block.hash()}")
    print(f"   Hash anterior:  {block.previous_hash}")
    print(f"   Transacciones:  {len(block.transactions)}")
    print(f"   Proposer:       {block.proposer_address}")
    print(f"   Firma proposer: {len(block.proposer_signature):,} bytes (ML-DSA-65)")


def cmd_chain_show(args: argparse.Namespace) -> None:
    chain = Chain(DATA_DIR)
    print(f"Altura:      {chain.height()} bloques")
    print(f"Mempool:     {len(chain.mempool)} transacciones pendientes")
    print(f"Cuentas:     {len(chain.state.accounts)} con saldo o nonce > 0")
    print(f"Ultimo hash: {chain.last_hash()}")


def cmd_chain_block(args: argparse.Namespace) -> None:
    chain = Chain(DATA_DIR)
    block = chain.get_block(args.index)
    if not block:
        print(f"ERROR: no existe el bloque #{args.index}", file=sys.stderr)
        sys.exit(1)
    print(_json.dumps(block.to_dict(), indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="qrb",
        description="QRB — prototipo Fase 0 (post-quantum blockchain demo)",
    )
    sub = parser.add_subparsers(dest="domain", required=True)

    # wallet
    w = sub.add_parser("wallet", help="Gestion de wallets")
    ws = w.add_subparsers(dest="action", required=True)
    wc = ws.add_parser("create", help="Crear una wallet nueva")
    wc.add_argument("--name", required=True)
    wc.set_defaults(func=cmd_wallet_create)
    wl = ws.add_parser("list", help="Listar wallets locales")
    wl.set_defaults(func=cmd_wallet_list)
    wb = ws.add_parser("balance", help="Consultar saldo de una direccion")
    wb.add_argument("--name", help="Nombre de wallet local")
    wb.add_argument("--address", help="Direccion externa (0x...)")
    wb.set_defaults(func=cmd_wallet_balance)

    # tx
    t = sub.add_parser("tx", help="Transacciones")
    ts = t.add_subparsers(dest="action", required=True)
    tsend = ts.add_parser("send", help="Enviar QRB de una wallet a una direccion")
    tsend.add_argument("--from", dest="sender", required=True)
    tsend.add_argument("--to", required=True)
    tsend.add_argument("--amount", type=int, required=True)
    tsend.set_defaults(func=cmd_tx_send)

    # chain
    c = sub.add_parser("chain", help="Operaciones sobre la cadena")
    cs = c.add_subparsers(dest="action", required=True)
    ci = cs.add_parser("init", help="Inicializar genesis con un fundador")
    ci.add_argument("--founder", required=True)
    ci.add_argument("--supply", type=int, required=True)
    ci.set_defaults(func=cmd_chain_init)
    cm = cs.add_parser("mine", help="Empaquetar mempool en un bloque firmado")
    cm.add_argument("--proposer", required=True)
    cm.set_defaults(func=cmd_chain_mine)
    csh = cs.add_parser("show", help="Resumen del estado de la cadena")
    csh.set_defaults(func=cmd_chain_show)
    cb = cs.add_parser("block", help="Mostrar un bloque por indice")
    cb.add_argument("--index", type=int, required=True)
    cb.set_defaults(func=cmd_chain_block)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
