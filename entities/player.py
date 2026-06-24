from dataclasses import dataclass, field


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
    # Animação de caminhada
    walk_textures: list = field(default_factory=list)  # Lista de texture_ids para frames de caminhada
    anim_timer: float = 0.0           # Tempo acumulado para trocar frame
    anim_frame: int = 0               # Índice do frame atual em walk_textures
    anim_speed: float = 0.15          # Segundos entre troca de frames
    is_moving: bool = False           # Se o jogador está andando neste frame

    def get_current_texture(self) -> int | None:
        """Retorna o texture_id correto baseado no estado de animação."""
        if self.is_moving and self.walk_textures:
            idx = self.anim_frame % len(self.walk_textures)
            return self.walk_textures[idx]
        return self.texture_id
