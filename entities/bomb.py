from dataclasses import dataclass

@dataclass
class Bomb:
    col: int
    row: int
    owner_id: int
    timer: float
    bomb_range: int
    collision_locked: bool = False
    texture_id: int | None = None
