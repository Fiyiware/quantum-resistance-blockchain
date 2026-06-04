"""Persistencia simple en JSON.

En producción esto sería una base de datos clave-valor (LevelDB,
RocksDB) con árboles de Merkle Patricia. Aquí es solo JSON para que
puedas inspeccionar fácilmente los archivos generados.
"""

import json
import sys
from pathlib import Path
from typing import Any


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))


def load_json(path: Path) -> Any:
    """Load JSON data from a file, raising a clear error if corrupt."""
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError) as exc:
        raise ValueError(
            f"could not read or parse {path} -- the file may be corrupt "
            f"(killed mid-write, or hand-edited). Try deleting or repairing it. "
            f"Details: {exc}"
        ) from exc
