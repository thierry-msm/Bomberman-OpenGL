# Sistema de Iluminação Simulada por Blending (Immediate Mode)

import math
from OpenGL.GL import *
import settings


def render_lighting(game_state):
    """
    Renderiza a camada de iluminação das explosões sobre a arena.
    
    1. Desenha overlay escuro semitransparente sobre toda a arena.
    2. Para cada explosão ativa, desenha luz radial aditiva com GL_TRIANGLE_FAN.
    3. Restaura o blend para o modo padrão ao final.
    """
    glDisable(GL_TEXTURE_2D)

    # Se não houver explosões ativas, pular todo o efeito de iluminação
    if not game_state.explosions:
        return

    # ── 1. Overlay escuro semitransparente sobre a arena ──
    # Usa blend padrão para escurecer
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    arena_top = settings.HUD_HEIGHT
    arena_bottom = settings.SCREEN_HEIGHT

    glColor4f(0.0, 0.0, 0.0, 0.45)
    glBegin(GL_QUADS)
    glVertex2f(0, arena_top)
    glVertex2f(settings.SCREEN_WIDTH, arena_top)
    glVertex2f(settings.SCREEN_WIDTH, arena_bottom)
    glVertex2f(0, arena_top)
    glEnd()

    # ── 2. Luzes radiais aditivas para cada explosão ativa ──
    # Troca para blend aditivo: a luz soma cor à cena
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)

    num_segments = 32  # Quantidade de segmentos do fan (resolução do círculo)

    for explosion in game_state.explosions:
        # Calcula o centro da explosão (média dos tiles afetados)
        if not explosion.tiles:
            continue

        # Intensidade proporcional ao tempo restante da explosão
        intensity = min(explosion.timer / 0.5, 1.0)

        for tile_col, tile_row in explosion.tiles:
            # Centro do tile em pixels
            cx = tile_col * settings.TILE_SIZE + settings.TILE_SIZE / 2.0
            cy = settings.HUD_HEIGHT + tile_row * settings.TILE_SIZE + settings.TILE_SIZE / 2.0

            # Raio de luz proporcional à propriedade light_radius e ao TILE_SIZE
            radius = explosion.light_radius * settings.TILE_SIZE * 0.5

            # Desenha fan radial: centro opaco, borda transparente
            glBegin(GL_TRIANGLE_FAN)

            # Vértice central — cor quente opaca (laranja incandescente)
            glColor4f(1.0, 0.6, 0.15, 0.7 * intensity)
            glVertex2f(cx, cy)

            # Vértices da borda — totalmente transparentes
            glColor4f(1.0, 0.3, 0.0, 0.0)
            for i in range(num_segments + 1):
                angle = 2.0 * math.pi * i / num_segments
                vx = cx + math.cos(angle) * radius
                vy = cy + math.sin(angle) * radius
                glVertex2f(vx, vy)

            glEnd()

    # ── 3. Restaurar blend padrão antes da HUD ──
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
