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
                # ESC retorna ao menu inicial
                game.state_manager.change_state(game.states["START_SCREEN"], game)

    def update(self, dt, game):
        pass

    def render(self, game):
        r, g, b, a = settings.COLOR_CLEAR_OVER
        glClearColor(r, g, b, a)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
