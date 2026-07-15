# QRB — Prototipo (Fase 0)

Prototipo de demostración de la **Quantum-Resistance Blockchain (QRB)**.

Implementa lo mínimo para mostrar que el modelo funciona: wallets post-cuánticas, transacciones firmadas con **ML-DSA-65** (estándar NIST FIPS 204, derivado de CRYSTALS-Dilithium), bloques encadenados y un estado de cuentas tipo Ethereum.

**No es producción.** No tiene red P2P, no tiene consenso descentralizado real, no tiene EVM. Es solo lo necesario para demostrar que las firmas post-cuánticas funcionan extremo a extremo y que el modelo de QRB es realizable.

## Requisitos

- Python 3.10 o superior
- pip

Comprueba tu versión:

```bash
python --version
```

Si tu versión es inferior a 3.10, instala una más reciente desde https://www.python.org/

## Instalación

Desde dentro de la carpeta `prototype/`:

```powershell
# (Recomendado) crear un entorno virtual aislado
python -m venv .venv

# Activar el entorno virtual en Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# (En macOS/Linux sería: source .venv/bin/activate)

# Instalar dependencias
pip install -r requirements.txt

# (Opcional) Instalar dependencias de desarrollo (pytest, linters)
pip install -r dev-requirements.txt
```

## Uso rápido — flujo completo

Una vez instaladas las dependencias:

```powershell
# 1. Crear wallets
python qrb_cli.py wallet create --name fundador
python qrb_cli.py wallet create --name alice
python qrb_cli.py wallet create --name bob

# 2. Inicializar la cadena con el fundador y su asignación inicial
python qrb_cli.py chain init --founder fundador --supply 1000000000

# 3. Listar wallets y direcciones
python qrb_cli.py wallet list

# 4. Consultar el saldo del fundador
python qrb_cli.py wallet balance --name fundador

# 5. Enviar QRB a Alice (coge la dirección de alice del paso 3)
python qrb_cli.py tx send --from fundador --to 0x... --amount 1000

# 6. Minar un bloque que incluya las transacciones pendientes
python qrb_cli.py chain mine --proposer fundador

# 7. Comprobar el nuevo saldo de Alice
python qrb_cli.py wallet balance --name alice

# 8. Inspeccionar el estado de la cadena
python qrb_cli.py chain show
python qrb_cli.py chain block --index 1
```

## Tests automáticos

Para verificar que todo funciona:

```bash
# (Recomendado) Usando pytest:
pip install -r dev-requirements.txt
pytest

# O sin pytest:
python tests/test_basic.py
```

Salida esperada (pytest):

```
============================= test session starts =============================
collected 15 items

tests/test_basic.py ............                                       [100%]

============================= 15 passed in 0.2s =============================
```

## Estructura del código

```
prototype/
├── qrb_cli.py              # Entrada por línea de comandos
├── requirements.txt        # Solo: dilithium-py
├── qrb/
│   ├── __init__.py
│   ├── crypto.py           # Wrappers de ML-DSA-65
│   ├── wallet.py           # Wallets y persistencia
│   ├── transaction.py      # Estructura y firma de transacciones
│   ├── block.py            # Bloques encadenados
│   ├── state.py            # Balances y nonces por cuenta
│   ├── storage.py          # JSON helpers
│   └── chain.py            # Orquesta cadena + estado + mempool
└── tests/
    └── test_basic.py       # Tests end-to-end
```

Los datos se guardan en `.qrb-data/` (creado automáticamente). Las wallets viven en `.qrb-data/wallets/` como JSON sin cifrar — **no usar en producción**.

## Qué demuestra este prototipo

1. Las firmas post-cuánticas **ML-DSA-65** son funcionales y verificables en una blockchain real (firmas de ~3,3 KB vs 64 bytes de ECDSA — factor ~50×).
2. El modelo account-based de Ethereum funciona con direcciones derivadas de hashes SHA3-256 de claves públicas PQ.
3. Un bloque QRB es estructuralmente idéntico a uno de Ethereum salvo por la primitiva de firma del proposer.
4. El tamaño real de las firmas y bloques se puede inspeccionar directamente en los JSON generados — útil para presentaciones y solicitudes de subvenciones.

## Qué NO hay (de momento)

- Red P2P entre nodos.
- Consenso descentralizado (este prototipo es *single-proposer*, solo un nodo).
- Máquina virtual EVM ni contratos inteligentes.
- Account Abstraction.
- Bridge a Ethereum.
- Cifrado de las claves privadas en disco.

Todo eso entra en **Fase 1** (testnet pública), una vez QRB obtenga los primeros grants.

## Licencia

MIT.
