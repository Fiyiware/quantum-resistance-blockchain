"""Persistencia simple en JSON.

En producción esto sería una base de datos clave-valor (LevelDB,
RocksDB) con árboles de Merkle Patricia. Aquí es solo JSON para que
puedas inspeccionar fácilmente los archivos generados.
"""

import json
from pathlib import Path
from typing import Any


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))


def load_json(path: Path) -> Any:
    """Load JSON data from a file with a friendly error message on corruption."""
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError) as exc:
        print(
            f"ERROR: Could not read or parse {path}. "
            f"The file may be corrupted (e.g. the process was killed mid-write, "
            f"or the JSON was hand-edited incorrectly).
"
            f"Try deleting or repairing the file, then run the command again.
"
            f"Details: {exc}",
            file=__import__("sys").stderr,
        )
        raise SystemExit(1)
