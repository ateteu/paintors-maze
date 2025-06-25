# ATTENTION:
# This code contains all classes initially proposed for the game. 
# Classes will be separated in separated codes in the future.

from abc import ABC, abstractmethod
from typing import Optional

# --- Core primitives ---

class Position:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        self._x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        self._y = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Position):
            return False
        return self.x == other.x and self.y == other.y


class Color:
    def __init__(self, name: str, rgb: tuple[int, int, int]):
        self._name = name
        self._rgb = rgb

    @property
    def name(self) -> str:
        return self._name

    @property
    def rgb(self) -> tuple[int, int, int]:
        return self._rgb

    def is_equal_to(self, other: "Color") -> bool:
        return self.name == other.name

    def combine_with(self, other: "Color") -> "Color":
        resultant_color = (
            COLOR_COMBINATIONS.get((self.name, other.name))
            or COLOR_COMBINATIONS.get((other.name, self.name))
            or self
        )
        return resultant_color

# Example color combination dictionary (to be customized)
COLOR_COMBINATIONS: dict[tuple[str, str], Color] = {
    ("blue", "green"): Color("yellow", (255, 255, 0)),
    ("red", "blue"): Color("purple", (128, 0, 128)),
    ("red", "green"): Color("brown", (139, 69, 19)),
}


# --- Base Entities ---

class GameEntity(ABC):
    def __init__(self, position: Position, color: Optional[Color] = None):
        self._position = position
        self._color = color
        self._active = True

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, value: Position) -> None:
        self._position = value

    @property
    def color(self) -> Optional[Color]:
        return self._color

    @color.setter
    def color(self, value: Color) -> None:
        self._color = value

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, value: bool) -> None:
        self._active = value

    @abstractmethod
    def update(self) -> None:
        pass


# --- Map Elements ---

class MapItem(GameEntity):
    @abstractmethod
    def is_passable(self, player_color: Optional[Color]) -> bool:
        pass


class Wall(MapItem):
    def is_passable(self, player_color: Optional[Color]) -> bool:
        return False

    def update(self) -> None:
        pass


class Door(MapItem):
    def is_passable(self, player_color: Optional[Color]) -> bool:
        if self.color is None or player_color is None:
            return False
        
        bool_value = self.color.is_equal_to(player_color)
        return bool_value

    def update(self) -> None:
        pass


class PaintingBlock(MapItem):
    def is_passable(self, player_color: Optional[Color]) -> bool:
        return True

    def interact(self, player: "Player") -> None:
        if self.color:
            player.change_color(self.color)

    def update(self) -> None:
        pass


# --- Player ---

class Player(GameEntity):
    def __init__(self, position: Position, speed: int = 1, color: Optional[Color] = None):
        super().__init__(position, color)
        self._speed = speed

    @property
    def speed(self) -> int:
        return self._speed

    @speed.setter
    def speed(self, new_value: int) -> None:
        self._speed = new_value

    def change_color(self, new_color: Color) -> None:
        if self.color:
            self.color = self.color.combine_with(new_color)
        else:
            self.color = new_color

    def update(self) -> None:
        pass
