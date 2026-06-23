import pygame
from OpenGL.GL import *
from state_manager import BaseState
import settings

class StartScreenState(BaseState):
    def enter(self, game):
        print("[State] Entrou no START_SCREEN. Placar zerado.")
        # Como especificado, ao entrar na tela inicial o placar geral deve ser zerado
        if hasattr(game, 'score_manager') and game.score_manager:
            game.score_manager.player1_wins = 0
            game.score_manager.player2_wins = 0

    def exit(self, game):
        print("[State] Saindo do START_SCREEN.")

    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                # Transição: pressionar ENTER vai para MATCH_PLAYING
                game.state_manager.change_state(game.states["MATCH_PLAYING"], game)

    def update(self, dt, game):
        pass

    def render(self, game):
        # Limpa com a cor definida em settings
        r, g, b, a = settings.COLOR_CLEAR_START
        glClearColor(r, g, b, a)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
