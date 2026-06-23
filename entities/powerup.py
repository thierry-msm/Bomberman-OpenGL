from dataclasses import dataclass

@dataclass
class PowerUp:
    col: int
    row: int
    type: str  # Pode ser "bomb_limit", "bomb_range" ou "speed"
