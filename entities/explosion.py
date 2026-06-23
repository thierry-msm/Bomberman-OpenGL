from dataclasses import dataclass

@dataclass
class Explosion:
    tiles: list  # Lista de tuplas (col, row) representando as posições da explosão no grid
    timer: float
    light_radius: float
