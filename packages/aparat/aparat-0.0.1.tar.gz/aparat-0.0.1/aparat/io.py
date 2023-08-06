import os
import tempfile
from typing import Any

from .rnd import random_alphanum


def file_write(path: str, data: Any, mode: str = 'w'):
    with open(path, mode) as f:
        f.write(data)
        f.close()


def file_read(path: str, mode='r') -> Any:
    with open(path, mode) as f:
        output = f.read()
        f.close()

    return output


def file_delete(path: str):
    os.unlink(path)


def rand_temp_file() -> str:
    p = os.path.join(tempfile.gettempdir(), random_alphanum(60))

    file_write(p, '')

    return p
