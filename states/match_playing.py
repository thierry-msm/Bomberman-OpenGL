import pygame
from OpenGL.GL import *
from state_manager import BaseState
import settings
from render.hud_renderer import draw_hud

class MatchPlayingState(BaseState):
    def enter(self, game):
        print("[State] Entrou no MATCH_PLAYING.")
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
        game.last_round_winner = winner_id
        if game.score_manager.has_champion():
            game.state_manager.change_state(game.states["GAME_OVER"], game)
        else:
            game.state_manager.change_state(game.states["ROUND_SCORE"], game)

    def update(self, dt, game):
        pass

    def render(self, game):
        # 1. Limpar fundo com verde
        r, g, b, a = settings.COLOR_CLEAR_PLAYING
        glClearColor(r, g, b, a)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # 2. Desenhar Arena Placeholder (abaixo da HUD)
        # Vamos desenhar um grid de fundo cinza escuro para simular a arena
        glDisable(GL_TEXTURE_2D)
        glColor4f(0.18, 0.22, 0.18, 1.0) # Verde oliva escuro/acinzentado
        glBegin(GL_QUADS)
        glVertex2f(0, settings.HUD_HEIGHT)
        glVertex2f(settings.SCREEN_WIDTH, settings.HUD_HEIGHT)
        glVertex2f(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        glVertex2f(0, settings.SCREEN_HEIGHT)
        glEnd()
        
        # 3. Desenhar a HUD do jogo
        draw_hud(game)
        
        # 4. Textos informativos / Simulação
        game.text_renderer.draw_text(
            text="ARENA DE COMBATE (Placeholder)",
            x=settings.SCREEN_WIDTH / 2.0,
            y=settings.HUD_HEIGHT + 100,
            size=28,
            color=(1.0, 1.0, 1.0),
            align="center"
        )
        
        simulation_lines = [
            "Use o teclado numérico ou alfa-numérico para simular a gameplay da Fase 3:",
            "",
            "Pressione '1' para: Vitória do Jogador 1 (Azul)",
            "Pressione '2' para: Vitória do Jogador 2 (Vermelho)",
            "Pressione '3' para: Empate na Rodada",
            "",
            "A gameplay principal e colisões serão implementadas na próxima etapa."
        ]
        for idx, line in enumerate(simulation_lines):
            game.text_renderer.draw_text(
                text=line,
                x=settings.SCREEN_WIDTH / 2.0,
                y=settings.HUD_HEIGHT + 180 + (idx * 30),
                size=18,
                color=(0.8, 0.9, 0.8),
                align="center"
            )
