# Renderizador Centralizado da Partida
#
# Ordem obrigatória de renderização (conforme especificação):
#   1. Fundo e mapa
#   2. Power-ups
#   3. Bombas
#   4. Explosões
#   5. Jogadores
#   6. Camada de iluminação (lighting.py)
#   7. HUD e textos (hud_renderer.py)

from OpenGL.GL import *
import settings
from render.texture_loader import draw_textured_quad
from render.lighting import render_lighting
from render.hud_renderer import draw_hud


# ── Helpers ──────────────────────────────────────────────────────────────────

def _draw_solid_quad(x, y, w, h, color):
    """Desenha um retângulo sólido com cor RGBA."""
    glColor4f(color[0], color[1], color[2], color[3])
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x, y + h)
    glEnd()


# ── Camadas individuais ─────────────────────────────────────────────────────

def _render_background_and_map(game_state):
    """Camada 1: Fundo da arena e blocos do mapa (geometria pura, sem texturas)."""
    glDisable(GL_TEXTURE_2D)

    tilemap = game_state.tilemap
    ts = settings.TILE_SIZE
    hud_h = settings.HUD_HEIGHT

    # Fundo verde escuro para as células livres
    _draw_solid_quad(0, hud_h, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT - hud_h,
                     (0.15, 0.22, 0.12, 1.0))

    for row_idx in range(tilemap.rows):
        for col_idx in range(tilemap.cols):
            tile = tilemap.get_tile(col_idx, row_idx)
            x = col_idx * ts
            y = hud_h + row_idx * ts

            if tile == 1:  # Parede indestrutível
                _draw_solid_quad(x, y, ts, ts, (0.22, 0.22, 0.22, 1.0))
                _draw_solid_quad(x + 3, y + 3, ts - 6, ts - 6, (0.32, 0.32, 0.32, 1.0))
                # Brilho superior para dar volume
                _draw_solid_quad(x + 3, y + 3, ts - 6, 4, (0.42, 0.42, 0.42, 1.0))
            elif tile == 2:  # Bloco destrutível (tijolo)
                _draw_solid_quad(x + 1, y + 1, ts - 2, ts - 2, (0.50, 0.25, 0.05, 1.0))
                _draw_solid_quad(x + 4, y + 4, ts - 8, ts - 8, (0.62, 0.33, 0.12, 1.0))
                # Linhas de "argamassa" horizontais e verticais para simular tijolos
                glColor4f(0.40, 0.20, 0.04, 1.0)
                glBegin(GL_QUADS)
                # Linha horizontal central
                glVertex2f(x + 2, y + ts / 2 - 1)
                glVertex2f(x + ts - 2, y + ts / 2 - 1)
                glVertex2f(x + ts - 2, y + ts / 2 + 1)
                glVertex2f(x + 2, y + ts / 2 + 1)
                # Linha vertical central
                glVertex2f(x + ts / 2 - 1, y + 2)
                glVertex2f(x + ts / 2 + 1, y + 2)
                glVertex2f(x + ts / 2 + 1, y + ts - 2)
                glVertex2f(x + ts / 2 - 1, y + ts - 2)
                glEnd()


def _render_powerups(game_state):
    """Camada 2: Power-ups no chão (geometria pura)."""
    glDisable(GL_TEXTURE_2D)

    ts = settings.TILE_SIZE
    hud_h = settings.HUD_HEIGHT
    margin = 14

    for pu in game_state.powerups:
        x = pu.col * ts + margin
        y = hud_h + pu.row * ts + margin
        sz = ts - margin * 2

        if pu.type == "bomb_limit":
            color = (0.85, 0.15, 0.85, 1.0)   # Magenta
            icon_color = (0.3, 0.0, 0.3, 1.0)
        elif pu.type == "bomb_range":
            color = (0.15, 0.85, 0.85, 1.0)   # Ciano
            icon_color = (0.0, 0.3, 0.3, 1.0)
        else:  # speed
            color = (0.90, 0.85, 0.10, 1.0)   # Amarelo
            icon_color = (0.4, 0.35, 0.0, 1.0)

        # Fundo do power-up
        _draw_solid_quad(x, y, sz, sz, color)
        # Ícone interno
        _draw_solid_quad(x + 8, y + 8, sz - 16, sz - 16, (1.0, 1.0, 1.0, 0.9))
        _draw_solid_quad(x + 12, y + 12, sz - 24, sz - 24, icon_color)


def _render_bombs(game_state):
    """Camada 3: Bombas (com textura se disponível, senão geometria)."""
    ts = settings.TILE_SIZE
    hud_h = settings.HUD_HEIGHT

    for bomb in game_state.bombs:
        x = bomb.col * ts
        y = hud_h + bomb.row * ts

        if bomb.texture_id is not None:
            # Renderizar com textura
            glEnable(GL_TEXTURE_2D)
            draw_textured_quad(bomb.texture_id, x, y, ts, ts)
            glDisable(GL_TEXTURE_2D)
        else:
            # Fallback: geometria colorida
            glDisable(GL_TEXTURE_2D)
            pad = 10
            # Corpo da bomba (preto)
            _draw_solid_quad(x + pad, y + pad, ts - pad * 2, ts - pad * 2, (0.08, 0.08, 0.08, 1.0))
            # Brilho especular
            _draw_solid_quad(x + pad + 6, y + pad + 4, 10, 8, (0.35, 0.35, 0.45, 1.0))
            # Pavio (laranja)
            _draw_solid_quad(x + ts // 2 - 3, y + pad - 8, 6, 10, (0.95, 0.55, 0.05, 1.0))
            # Faísca no pavio (amarelo piscante proporcional ao timer)
            spark_alpha = 0.5 + 0.5 * (1.0 if int(bomb.timer * 6) % 2 == 0 else 0.0)
            _draw_solid_quad(x + ts // 2 - 4, y + pad - 12, 8, 6, (1.0, 1.0, 0.2, spark_alpha))


def _render_explosions(game_state):
    """Camada 4: Explosões (geometria colorida pura)."""
    glDisable(GL_TEXTURE_2D)

    ts = settings.TILE_SIZE
    hud_h = settings.HUD_HEIGHT

    for explosion in game_state.explosions:
        # Intensidade baseada no timer restante
        t = min(explosion.timer / 0.5, 1.0)

        for tile_col, tile_row in explosion.tiles:
            x = tile_col * ts
            y = hud_h + tile_row * ts

            # Camada exterior — laranja
            _draw_solid_quad(x, y, ts, ts, (1.0, 0.35, 0.0, 0.85 * t))
            # Camada intermediária — amarelo quente
            _draw_solid_quad(x + 8, y + 8, ts - 16, ts - 16, (1.0, 0.75, 0.1, 0.9 * t))
            # Núcleo central — branco quente
            _draw_solid_quad(x + 16, y + 16, ts - 32, ts - 32, (1.0, 1.0, 0.8, 0.95 * t))


def _render_players(game_state):
    """Camada 5: Jogadores (com textura se disponível, senão geometria)."""
    ts = settings.TILE_SIZE
    hud_h = settings.HUD_HEIGHT

    for player in game_state.players.values():
        if not player.alive:
            continue

        x = player.col * ts
        y = hud_h + player.row * ts

        if player.texture_id is not None:
            # Obter textura correta baseada no estado de animação
            current_tex = player.get_current_texture()
            # Renderizar com textura
            glEnable(GL_TEXTURE_2D)
            draw_textured_quad(current_tex, x, y, ts, ts)
            glDisable(GL_TEXTURE_2D)
        else:
            # Fallback: geometria colorida com detalhes faciais
            glDisable(GL_TEXTURE_2D)
            pad = 6

            # Cor base: Azul para P1, Vermelho para P2
            if player.id == 1:
                body_color = (0.20, 0.55, 1.0, 1.0)
                dark_color = (0.10, 0.35, 0.70, 1.0)
            else:
                body_color = (1.0, 0.30, 0.30, 1.0)
                dark_color = (0.70, 0.15, 0.15, 1.0)

            # Corpo
            _draw_solid_quad(x + pad, y + pad, ts - pad * 2, ts - pad * 2, body_color)
            # Sombra inferior para volume
            _draw_solid_quad(x + pad, y + ts - pad - 6, ts - pad * 2, 6, dark_color)

            # Rosto — olhos brancos
            eye_w, eye_h = 10, 10
            eye_y = y + pad + 8
            _draw_solid_quad(x + pad + 8, eye_y, eye_w, eye_h, (1.0, 1.0, 1.0, 1.0))
            _draw_solid_quad(x + ts - pad - 8 - eye_w, eye_y, eye_w, eye_h, (1.0, 1.0, 1.0, 1.0))

            # Pupilas pretas
            pupil_w, pupil_h = 4, 5
            _draw_solid_quad(x + pad + 12, eye_y + 3, pupil_w, pupil_h, (0.0, 0.0, 0.0, 1.0))
            _draw_solid_quad(x + ts - pad - 12, eye_y + 3, pupil_w, pupil_h, (0.0, 0.0, 0.0, 1.0))

            # Boca (sorriso simples)
            _draw_solid_quad(x + pad + 12, y + pad + 28, ts - pad * 2 - 24, 4, dark_color)


# ── Pipeline principal ───────────────────────────────────────────────────────

def render_match(game):
    """
    Pipeline centralizado de renderização da partida.
    Respeita estritamente a ordem de camadas definida na especificação.
    """
    gs = game.game_state

    # Limpar tela
    r, g, b, a = settings.COLOR_CLEAR_PLAYING
    glClearColor(r, g, b, a)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # 1. Fundo e mapa
    _render_background_and_map(gs)

    # 2. Power-ups
    _render_powerups(gs)

    # 3. Bombas
    _render_bombs(gs)

    # 4. Explosões
    _render_explosions(gs)

    # 5. Jogadores
    _render_players(gs)

    # 6. Camada de iluminação (lighting.py)
    render_lighting(gs)

    # 7. HUD e textos (desenhados por último para não serem escurecidos)
    glDisable(GL_TEXTURE_2D)
    draw_hud(game)
