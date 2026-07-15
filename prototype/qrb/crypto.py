"""Primitivas criptográficas post-cuánticas para QRB.

Usa ML-DSA-65 (estándar NIST FIPS 204, agosto 2024).
Equivalente al nivel de seguridad 3 de CRYSTALS-Dilithium.

Nivel de seguridad: ~AES-192 frente a ataques cuánticos.
Tamaños aproximados:
  - Clave pública: 1.952 bytes
  - Clave privada: 4.032 bytes
  - Firma:         3.309 bytes

Compárese con ECDSA secp256k1 (Ethereum/Bitcoin):
  - Clave pública: 33 bytes
  - Clave privada: 32 bytes
  - Firma:         64 bytes

El precio de la resistencia cuántica es un factor ~50× en tamaño. Esos bytes
van a la capa de disponibilidad de datos (DA) igualmente: la Account
Abstraction mejora la UX y la rotación de claves, pero NO reduce ese coste.
La palanca real para reducirlo es la verificación en lote / agregación dentro
de pruebas STARK (visión Fase 3+).

⚠️ Nota de implementación: `dilithium-py` es una implementación de REFERENCIA
en Python puro, para claridad e inspección, NO para producción: no ofrece
garantías de tiempo constante ni resistencia a side-channels. Para un
precompilado de VERIFICACIÓN esto importa poco (todo es dato público); para
FIRMAR en wallets de producción se usaría una implementación endurecida.
"""

import hashlib

from dilithium_py.ml_dsa import ML_DSA_65

SIGNATURE_SCHEME = "ML-DSA-65"


def generate_keypair() -> tuple[bytes, bytes]:
    """Genera un par de claves ML-DSA-65.

    Returns:
        (public_key, private_key) como bytes.
    """
    pk, sk = ML_DSA_65.keygen()
    return pk, sk


def sign(message: bytes, private_key: bytes) -> bytes:
    """Firma un mensaje con clave privada ML-DSA-65.

    Args:
        message: bytes a firmar (típicamente el payload serializado
                 de una transacción o cabecera de bloque).
        private_key: clave privada del firmante.

    Returns:
        Firma desadjuntada (~3.309 bytes).
    """
    return ML_DSA_65.sign(private_key, message)


def verify(message: bytes, signature: bytes, public_key: bytes) -> bool:
    """Verifica una firma ML-DSA-65.

    Args:
        message: mensaje original.
        signature: firma a verificar.
        public_key: clave pública del firmante esperado.

    Returns:
        True si la firma es válida y corresponde a la clave dada,
        False en cualquier otro caso (incluida excepción).
    """
    try:
        return bool(ML_DSA_65.verify(public_key, message, signature))
    except Exception:
        return False


def address_from_pubkey(public_key: bytes) -> str:
    """Deriva una dirección QRB del hash de la clave pública.

    Igual que en Bitcoin y Ethereum modernos, las direcciones son el
    hash de la clave pública, no la clave pública en sí. Esto oculta
    la pubkey hasta el primer gasto desde esa dirección, lo cual es
    especialmente relevante en el contexto post-cuántico
    ('harvest now, decrypt later').

    Formato: '0x' + últimos 20 bytes del SHA3-256 de la pubkey, en hex.
    Total: 42 caracteres (compatible con la convención de Ethereum).

    Args:
        public_key: clave pública ML-DSA-65 en bytes.

    Returns:
        Dirección con prefijo '0x' y 40 hex chars.
    """
    h = hashlib.sha3_256(public_key).digest()
    return "0x" + h[-20:].hex()


def is_valid_address(address: str) -> bool:
    """Comprueba que una cadena tiene el formato de dirección QRB.

    Una dirección válida es '0x' seguido de 40 caracteres hexadecimales
    (los últimos 20 bytes de un SHA3-256), igual que la convención de
    Ethereum. No comprueba que exista una cuenta con esa dirección, solo
    que el formato es correcto — suficiente para evitar enviar fondos a
    una dirección malformada e irrecuperable.

    Args:
        address: cadena a comprobar.

    Returns:
        True si el formato es válido, False en caso contrario.
    """
    if not isinstance(address, str) or not address.startswith("0x"):
        return False
    hex_part = address[2:]
    if len(hex_part) != 40:
        return False
    try:
        bytes.fromhex(hex_part)
    except ValueError:
        return False
    return True
