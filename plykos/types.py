from dataclasses import dataclass
from re import compile
from typing import Self

_PAGE_TITLE_REGEX = compile(
    r"^Keys:(?P<codename>[A-Za-z0-9]+)\s+(?P<buildid>[A-Za-z0-9]+)\s+\((?P<identifier>[A-Za-z0-9,]+)\)$"
)


@dataclass(frozen=True)
class Component:
    name: str
    filename: str
    key: bytes
    iv: bytes

    def __repr__(self) -> str:
        return f'Component(name={self.name}, file={self.filename}, key={self.key.hex()}, iv={self.iv.hex()})'


@dataclass(frozen=True)
class Firmware:
    identifier: str
    buildid: str
    codename: str
    components: tuple[Component]

    def __repr__(self) -> str:
        return f'Firmware(id={self.identifier}, buildid={self.buildid}, codename={self.codename}, components={", ".join(c.name for c in self.components)})'

    @classmethod
    def from_page_title(cls, title: str, components: list[Component]) -> Self:
        if (match := _PAGE_TITLE_REGEX.match(title)) is None:
            raise ValueError(f'Invalid title provided: {title}')

        return cls(components=components, **match.groupdict())
