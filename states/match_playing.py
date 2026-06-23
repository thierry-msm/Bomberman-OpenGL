import pygame
from OpenGL.GL import *
from state_manager import BaseState
import settings

class MatchPlayingState(BaseState):
    def enter(self, game):
        print("[State] Entrou no MATCH_PLAYING.")
        # O estado interno da rodada deve ser recriado (placeholder por enquanto)
        self.round_ended = False

    def exit(self, game):
        print("[State] Saindo do MATCH_PLAYING.")

    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN:
            # Lógica temporária de teste para simular fim de rodada
            if event.key == pygame.K_1:
                print("Simulando: Jogador 1 venceu a rodada!")
                game.score_manager.add_win(1)
                self._handle_round_end(game, winner_id=1)
            elif event.key == pygame.K_2:
                print("Simulando: Jogador 2 venceu a rodada!")
                game.score_manager.add_win(2)
                self._handle_round_end(game, winner_id=2)
            elif event.key == pygame.K_3:
                print("Simulando: Rodada empatada!")
                self._handle_round_end(game, winner_id=None)

    def _handle_round_end(self, game, winner_id):
        # Armazena o resultado da última rodada para exibir no ROUND_SCORE ou GAME_OVER
        game.last_round_winner = winner_id
        
        # Verifica se alguém atingiu a meta de 5 vitórias
        if game.score_manager.has_champion():
            game.state_manager.change_state(game.states["GAME_OVER"], game)
        else:
            game.state_manager.change_state(game.states["ROUND_SCORE"], game)

    def update(self, dt, game):
        # No futuro, o movimento contínuo dos jogadores usando pygame.key.get_pressed() será processado aqui.
        pass

    def render(self, game):
        r, g, b, a = settings.COLOR_CLEAR_PLAYING
        glClearColor(r, g, b, a)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
