from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    nome: str
    nomeusuario: str
    senha: str
    id: Optional[int] = None
