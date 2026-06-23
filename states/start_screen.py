import pygame
from OpenGL.GL import *
from state_manager import BaseState
import settings

class StartScreenState(BaseState):
    def enter(self, game):
        print("[State] Entrou no START_SCREEN. Placar zerado.")
        # Zera placar geral ao entrar na tela inicial
        if hasattr(game, 'score_manager') and game.score_manager:
            game.score_manager.player1_wins = 0
            game.score_manager.player2_wins = 0

    def exit(self, game):
        print("[State] Saindo do START_SCREEN.")

    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                game.state_manager.change_state(game.states["MATCH_PLAYING"], game)

    def update(self, dt, game):
        pass

    def render(self, game):
        # Limpar com azul escuro
        r, g, b, a = settings.COLOR_CLEAR_START
        glClearColor(r, g, b, a)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # 1. Título do Jogo
        game.text_renderer.draw_text(
            text="BOMBERMAN 2D",
            x=settings.SCREEN_WIDTH / 2.0,
            y=120,
            size=56,
            color=(0.95, 0.8, 0.1),  # Dourado brilhante
            align="center"
        )
        
        game.text_renderer.draw_text(
            text="Desafio OpenGL 2D Multiplayer Local",
            x=settings.SCREEN_WIDTH / 2.0,
            y=190,
            size=18,
            color=(0.7, 0.8, 0.9),  # Azul esbranquiçado
            align="center"
        )
        
        # Linha separadora decorativa
        glDisable(GL_TEXTURE_2D)
        glColor4f(0.85, 0.65, 0.15, 0.3)
        glBegin(GL_QUADS)
        glVertex2f(settings.SCREEN_WIDTH / 2.0 - 150, 220)
        glVertex2f(settings.SCREEN_WIDTH / 2.0 + 150, 220)
        glVertex2f(settings.SCREEN_WIDTH / 2.0 + 150, 222)
        glVertex2f(settings.SCREEN_WIDTH / 2.0 - 150, 222)
        glEnd()
        
        # 2. Controles do Jogador 1 (Esquerda)
        game.text_renderer.draw_text(
            text="JOGADOR 1 (Azul)",
            x=settings.SCREEN_WIDTH * 0.25,
            y=280,
            size=24,
            color=(0.3, 0.7, 1.0),
            align="center"
        )
        controls_p1 = [
            "Mover: W, A, S, D",
            "Plantar Bomba: ESPAÇO",
            "Power-ups aumentam força e velocidade"
        ]
        for idx, line in enumerate(controls_p1):
            game.text_renderer.draw_text(
                text=line,
                x=settings.SCREEN_WIDTH * 0.25,
                y=330 + (idx * 35),
                size=18,
                color=(0.8, 0.85, 0.9),
                align="center"
            )
            
        # 3. Controles do Jogador 2 (Direita)
        game.text_renderer.draw_text(
            text="JOGADOR 2 (Vermelho)",
            x=settings.SCREEN_WIDTH * 0.75,
            y=280,
            size=24,
            color=(1.0, 0.4, 0.4),
            align="center"
        )
        controls_p2 = [
            "Mover: SETAS DO TECLADO",
            "Plantar Bomba: ENTER",
            "Cuidado para não se encurralar!"
        ]
        for idx, line in enumerate(controls_p2):
            game.text_renderer.draw_text(
                text=line,
                x=settings.SCREEN_WIDTH * 0.75,
                y=330 + (idx * 35),
                size=18,
                color=(0.8, 0.85, 0.9),
                align="center"
            )
            
        # 4. Meta de vitória
        game.text_renderer.draw_text(
            text=f"Meta: O primeiro a obter {game.score_manager.target_wins} vitórias vence a disputa!",
            x=settings.SCREEN_WIDTH / 2.0,
            y=500,
            size=18,
            color=(0.9, 0.9, 0.1),
            align="center"
        )
        
        # 5. Instrução de início
        # Efeito de piscar simples baseada em tempo (opcional/micro-animação simulada)
        # Vamos manter o texto estático bem contrastado por enquanto
        game.text_renderer.draw_text(
            text="Pressione ENTER para iniciar a batalha",
            x=settings.SCREEN_WIDTH / 2.0,
            y=580,
            size=26,
            color=(1.0, 1.0, 1.0),
            align="center"
        )
