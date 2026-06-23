from dataclasses import dataclass

@dataclass
class Player:
    id: int
    col: float
    row: float
    speed: float
    bomb_limit: int
    bomb_range: int
    alive: bool
    texture_id: int | None = None
