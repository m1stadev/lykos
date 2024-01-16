from dataclasses import dataclass


@dataclass(frozen=True)
class Component:
    name: str
    key: bytes
    iv: bytes

    def __repr__(self) -> str:
        return f'Component(name={self.name}, key={self.key.hex()}, iv={self.iv.hex()})'
