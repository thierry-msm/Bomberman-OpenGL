import pygame
from OpenGL.GL import *
from state_manager import BaseState
import settings

class RoundScoreState(BaseState):
    def enter(self, game):
        print(f"[State] Entrou no ROUND_SCORE. Placar atual - P1: {game.score_manager.player1_wins} | P2: {game.score_manager.player2_wins}")

    def exit(self, game):
        print("[State] Saindo do ROUND_SCORE.")

    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                # Retorna para o jogo para iniciar a próxima rodada
                game.state_manager.change_state(game.states["MATCH_PLAYING"], game)

    def update(self, dt, game):
        pass

    def render(self, game):
        # Limpar com marrom escuro
        r, g, b, a = settings.COLOR_CLEAR_SCORE
        glClearColor(r, g, b, a)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # 1. Anúncio do Vencedor da Rodada
        winner = game.last_round_winner
        if winner == 1:
            winner_text = "JOGADOR 1 VENCEU A RODADA!"
            color_text = (0.3, 0.7, 1.0)
        elif winner == 2:
            winner_text = "JOGADOR 2 VENCEU A RODADA!"
            color_text = (1.0, 0.4, 0.4)
        else:
            winner_text = "RODADA EMPATADA!"
            color_text = (0.8, 0.8, 0.8)
            
        game.text_renderer.draw_text(
            text=winner_text,
            x=settings.SCREEN_WIDTH / 2.0,
            y=120,
            size=36,
            color=color_text,
            align="center"
        )
        
        # 2. Subtítulo decorativo
        game.text_renderer.draw_text(
            text="Placar Parcial da Disputa",
            x=settings.SCREEN_WIDTH / 2.0,
            y=190,
            size=18,
            color=(0.7, 0.7, 0.7),
            align="center"
        )
        
        # 3. Painel do Placar Lado a Lado
        # Desenha caixas de fundo para o placar dos jogadores
        glDisable(GL_TEXTURE_2D)
        # Caixa P1
        glColor4f(0.1, 0.15, 0.25, 0.5)
        glBegin(GL_QUADS)
        glVertex2f(settings.SCREEN_WIDTH * 0.2, 250)
        glVertex2f(settings.SCREEN_WIDTH * 0.45, 250)
        glVertex2f(settings.SCREEN_WIDTH * 0.45, 450)
        glVertex2f(settings.SCREEN_WIDTH * 0.2, 450)
        glEnd()
        
        # Caixa P2
        glColor4f(0.25, 0.1, 0.1, 0.5)
        glBegin(GL_QUADS)
        glVertex2f(settings.SCREEN_WIDTH * 0.55, 250)
        glVertex2f(settings.SCREEN_WIDTH * 0.8, 250)
        glVertex2f(settings.SCREEN_WIDTH * 0.8, 450)
        glVertex2f(settings.SCREEN_WIDTH * 0.55, 450)
        glEnd()
        
        # Textos de Placar
        # P1
        game.text_renderer.draw_text(
            text="JOGADOR 1",
            x=settings.SCREEN_WIDTH * 0.325,
            y=270,
            size=20,
            color=(0.3, 0.7, 1.0),
            align="center"
        )
        game.text_renderer.draw_text(
            text=str(game.score_manager.player1_wins),
            x=settings.SCREEN_WIDTH * 0.325,
            y=310,
            size=80,
            color=(1.0, 1.0, 1.0),
            align="center"
        )
        
        # P2
        game.text_renderer.draw_text(
            text="JOGADOR 2",
            x=settings.SCREEN_WIDTH * 0.675,
            y=270,
            size=20,
            color=(1.0, 0.4, 0.4),
            align="center"
        )
        game.text_renderer.draw_text(
            text=str(game.score_manager.player2_wins),
            x=settings.SCREEN_WIDTH * 0.675,
            y=310,
            size=80,
            color=(1.0, 1.0, 1.0),
            align="center"
        )
        
        # 4. Meta / Informações adicionais
        game.text_renderer.draw_text(
            text=f"Meta geral: {game.score_manager.target_wins} vitórias",
            x=settings.SCREEN_WIDTH / 2.0,
            y=500,
            size=18,
            color=(0.9, 0.9, 0.1),
            align="center"
        )
        
        # 5. Instrução de continuação
        game.text_renderer.draw_text(
            text="Pressione ENTER para continuar a disputa",
            x=settings.SCREEN_WIDTH / 2.0,
            y=580,
            size=24,
            color=(1.0, 1.0, 1.0),
            align="center"
        )
