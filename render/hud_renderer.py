from OpenGL.GL import *
import settings

def draw_hud(game):
    """Desenha a barra superior de HUD contendo o placar atual e status da disputa."""
    # 1. Desenhar a barra sólida da HUD (texturas desativadas)
    glDisable(GL_TEXTURE_2D)
    
    # Retângulo de fundo (cinza grafite escuro)
    glColor4f(0.12, 0.12, 0.12, 1.0)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(settings.SCREEN_WIDTH, 0)
    glVertex2f(settings.SCREEN_WIDTH, settings.HUD_HEIGHT)
    glVertex2f(0, settings.HUD_HEIGHT)
    glEnd()
    
    # Linha de divisão inferior (dourada)
    glColor4f(0.85, 0.65, 0.15, 1.0)
    glBegin(GL_QUADS)
    glVertex2f(0, settings.HUD_HEIGHT - 4)
    glVertex2f(settings.SCREEN_WIDTH, settings.HUD_HEIGHT - 4)
    glVertex2f(settings.SCREEN_WIDTH, settings.HUD_HEIGHT)
    glVertex2f(0, settings.HUD_HEIGHT)
    glEnd()
    
    # 2. Renderizar os textos sobre a HUD utilizando o text_renderer do jogo
    p1_wins = game.score_manager.player1_wins
    p2_wins = game.score_manager.player2_wins
    
    # Placar Jogador 1 (Azul)
    game.text_renderer.draw_text(
        text=f"P1 (W/A/S/D): {p1_wins} / {game.score_manager.target_wins}",
        x=20,
        y=18,
        size=22,
        color=(0.3, 0.6, 1.0),
        align="left"
    )
    
    # Placar Jogador 2 (Vermelho)
    game.text_renderer.draw_text(
        text=f"P2 (Setas): {p2_wins} / {game.score_manager.target_wins}",
        x=settings.SCREEN_WIDTH - 20,
        y=18,
        size=22,
        color=(1.0, 0.4, 0.4),
        align="right"
    )
    
    # Indicador de Rodada / Objetivo no Centro (Amarelo)
    game.text_renderer.draw_text(
        text="DISPUTA ATIVA",
        x=settings.SCREEN_WIDTH / 2.0,
        y=18,
        size=18,
        color=(0.9, 0.9, 0.1),
        align="center"
    )
