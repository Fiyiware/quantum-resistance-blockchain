"""Persistencia simple en JSON.

En producción esto sería una base de datos clave-valor (LevelDB,
RocksDB) con árboles de Merkle Patricia. Aquí es solo JSON para que
puedas inspeccionar fácilmente los archivos generados.
"""

import json
import os
import tempfile
from pathlib import Path
from typing import Any


def save_json(path: Path, data: Any) -> None:
    """Escribe JSON de forma atómica: a un temporal en el mismo directorio y
    luego os.replace (rename atómico en POSIX/NTFS). Así un corte a mitad de
    escritura no deja el archivo a medias ni desincroniza unos ficheros con
    otros."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(json.dumps(data, indent=2))
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def load_json(path: Path) -> Any:
    """Carga JSON desde un archivo, lanzando un error claro que nombra el
    archivo si está corrupto (proceso cortado a mitad de escritura, JSON
    editado a mano, etc.). El CLI convierte el ValueError en 'ERROR: ...'
    con código de salida 1."""
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError) as exc:
        raise ValueError(
            f"no se pudo leer o parsear {path} -- el archivo puede estar "
            f"corrupto (proceso cortado a mitad de escritura, o editado a mano). "
            f"Prueba a borrarlo o repararlo. Detalles: {exc}"
        ) from exc
