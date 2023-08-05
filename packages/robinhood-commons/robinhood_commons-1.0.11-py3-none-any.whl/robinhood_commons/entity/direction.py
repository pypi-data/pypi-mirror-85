from __future__ import annotations

from enum import Enum, auto

from robinhood_commons.entity.printable import Printable


class Direction(Printable, Enum):
    UP = auto()
    DOWN = auto()
    NEUTRAL = auto()

    @staticmethod
    def to_enum(value: str) -> Direction:
        v: str = value.upper()
        return Direction[v]

    def value(self) -> str:
        return self.name.lower()


def main() -> None:
    print(Direction.to_enum("down"))
    print(Direction.to_enum("neutral"))
    print(Direction.UP.value())


if __name__ == "__main__":
    main()
