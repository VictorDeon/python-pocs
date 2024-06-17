from dataclasses import dataclass, asdict, fields
from typing import Optional, Any


@dataclass
class Pokemon:
    id: int
    name: str
    sprites: Optional[dict[str, Any]] = None
    height: Optional[int] = None
    weight: Optional[float | int] = None
    types: Optional[list[dict[str, Any]]] = None
    weaknesses: Optional[list[str]] = None
    stats: Optional[list[dict[str, Any]]] = None
    abilities: Optional[list[dict[str, Any]]] = None
    species: Optional[dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data):
        return cls(**{f.name: data.get(f.name) for f in fields(cls)})

    def to_dict(self):
        return asdict(self)
