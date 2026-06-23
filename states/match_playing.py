import pygame
from OpenGL.GL import *
from state_manager import BaseState
import settings
from core.game_state import GameState
from core.round_manager import check_round_end
from render.renderer import render_match


class MatchPlayingState(BaseState):
    def enter(self, game):
        print("[State] Entrou no MATCH_PLAYING. Inicializando rodada...")
        # Cria um novo estado limpo de jogo/rodada
        game.game_state = GameState()
        self.round_ended = False

    def exit(self, game):
        print("[State] Saindo do MATCH_PLAYING.")

    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN:
            # Pressionar SPACE planta bomba para o Jogador 1
            if event.key == pygame.K_SPACE:
                game.game_state.plant_bomb(1)
            # Pressionar ENTER (comum ou teclado numérico) planta bomba para o Jogador 2
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                game.game_state.plant_bomb(2)
            # Tecla ESC volta ao menu inicial
            elif event.key == pygame.K_ESCAPE:
                game.state_manager.change_state(game.states["START_SCREEN"], game)

    def update(self, dt, game):
        if self.round_ended:
            return

        # 1. Obter estado contínuo de teclas pressionadas para movimentação
        pressed_keys = pygame.key.get_pressed()

        # 2. Atualizar estado interno de física e lógica do jogo
        game.game_state.update(dt, pressed_keys)

        # 3. Verificar fim de rodada usando o RoundManager
        result = check_round_end(game.game_state.players)
        if result is not None:
            self.round_ended = True
            print(f"[MatchPlaying] Fim de rodada detectado: {result.message}")

            # Atualiza placar acumulado se houve vencedor (não empate)
            if result.winner_id is not None:
                game.score_manager.add_win(result.winner_id)

            # Registra o resultado para a tela de pontuação
            game.last_round_winner = result.winner_id

            # Decisão de transição de tela
            if game.score_manager.has_champion():
                game.state_manager.change_state(game.states["GAME_OVER"], game)
            else:
                game.state_manager.change_state(game.states["ROUND_SCORE"], game)

    def render(self, game):
        # Delega toda a renderização ao pipeline centralizado do renderer.py
        render_match(game)
