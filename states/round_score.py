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
                # Se ninguém chegou a 5 vitórias, ENTER inicia a próxima rodada
                game.state_manager.change_state(game.states["MATCH_PLAYING"], game)

    def update(self, dt, game):
        pass

    def render(self, game):
        r, g, b, a = settings.COLOR_CLEAR_SCORE
        glClearColor(r, g, b, a)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
