import pygame
from OpenGL.GL import *
from state_manager import BaseState
import settings

class GameOverState(BaseState):
    def enter(self, game):
        champion = game.score_manager.get_champion()
        print(f"[State] Entrou no GAME_OVER. Campeão Geral: Jogador {champion}! Placar final - P1: {game.score_manager.player1_wins} | P2: {game.score_manager.player2_wins}")

    def exit(self, game):
        print("[State] Saindo do GAME_OVER.")

    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                print("Reiniciando disputa...")
                # R reinicia a disputa completa: zera placar e vai para MATCH_PLAYING
                game.score_manager.player1_wins = 0
                game.score_manager.player2_wins = 0
                game.state_manager.change_state(game.states["MATCH_PLAYING"], game)
            elif event.key == pygame.K_ESCAPE:
                print("Voltando ao menu principal...")
                game.state_manager.change_state(game.states["START_SCREEN"], game)

    def update(self, dt, game):
        pass

    def render(self, game):
        # Limpar com vermelho escuro
        r, g, b, a = settings.COLOR_CLEAR_OVER
        glClearColor(r, g, b, a)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        champion = game.score_manager.get_champion()
        
        # 1. Anúncio de Campeão
        if champion == 1:
            color_winner = (0.3, 0.7, 1.0)
            winner_text = "JOGADOR 1 É O CAMPEÃO GERAL!"
        elif champion == 2:
            color_winner = (1.0, 0.4, 0.4)
            winner_text = "JOGADOR 2 É O CAMPEÃO GERAL!"
        else:
            color_winner = (0.9, 0.9, 0.9)
            winner_text = "DISPUTA SEM CAMPEÃO!"
            
        game.text_renderer.draw_text(
            text="FIM DE DISPUTA",
            x=settings.SCREEN_WIDTH / 2.0,
            y=100,
            size=48,
            color=(0.95, 0.8, 0.1),
            align="center"
        )
        
        game.text_renderer.draw_text(
            text=winner_text,
            x=settings.SCREEN_WIDTH / 2.0,
            y=170,
            size=28,
            color=color_winner,
            align="center"
        )
        
        # 2. Painel de Placar Final
        # Caixa central cinza translúcida
        glDisable(GL_TEXTURE_2D)
        glColor4f(0.08, 0.08, 0.08, 0.7)
        glBegin(GL_QUADS)
        glVertex2f(settings.SCREEN_WIDTH * 0.25, 230)
        glVertex2f(settings.SCREEN_WIDTH * 0.75, 230)
        glVertex2f(settings.SCREEN_WIDTH * 0.75, 430)
        glVertex2f(settings.SCREEN_WIDTH * 0.25, 430)
        glEnd()
        
        # Textos do Placar Final
        game.text_renderer.draw_text(
            text="RESULTADO FINAL",
            x=settings.SCREEN_WIDTH / 2.0,
            y=250,
            size=18,
            color=(0.7, 0.7, 0.7),
            align="center"
        )
        
        score_text = f"{game.score_manager.player1_wins}   X   {game.score_manager.player2_wins}"
        game.text_renderer.draw_text(
            text=score_text,
            x=settings.SCREEN_WIDTH / 2.0,
            y=290,
            size=72,
            color=(1.0, 1.0, 1.0),
            align="center"
        )
        
        game.text_renderer.draw_text(
            text="Jogador 1 (Azul)              Jogador 2 (Vermelho)",
            x=settings.SCREEN_WIDTH / 2.0,
            y=380,
            size=16,
            color=(0.6, 0.8, 0.9),
            align="center"
        )
        
        # 3. Instruções de Replay / Menu
        game.text_renderer.draw_text(
            text="Pressione R para reiniciar a disputa completa",
            x=settings.SCREEN_WIDTH / 2.0,
            y=520,
            size=20,
            color=(1.0, 1.0, 1.0),
            align="center"
        )
        
        game.text_renderer.draw_text(
            text="Pressione ESC para voltar ao Menu Inicial",
            x=settings.SCREEN_WIDTH / 2.0,
            y=570,
            size=20,
            color=(0.7, 0.7, 0.7),
            align="center"
        )
