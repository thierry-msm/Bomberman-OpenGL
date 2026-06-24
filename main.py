import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *

import settings
from state_manager import StateManager
from core.score_manager import ScoreManager
from render.text_renderer import TextRenderer
from states.start_screen import StartScreenState
from states.match_playing import MatchPlayingState
from states.round_score import RoundScoreState
from states.game_over import GameOverState

class Game:
    def __init__(self):
        pygame.init()
        # Inicializa a janela com Pygame + contexto OpenGL
        pygame.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT),
            DOUBLEBUF | OPENGL
        )
        pygame.display.set_caption("Bomberman 2D OpenGL")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Configuração do OpenGL
        self._init_opengl()
        
        # Renderizador de Textos
        self.text_renderer = TextRenderer()
        
        # Gerenciamento de Pontos
        self.score_manager = ScoreManager()
        self.last_round_winner = None
        
        # Gerenciamento de Estados
        self.state_manager = StateManager()
        self.states = {
            "START_SCREEN": StartScreenState(),
            "MATCH_PLAYING": MatchPlayingState(),
            "ROUND_SCORE": RoundScoreState(),
            "GAME_OVER": GameOverState()
        }
        
        # Inicia no estado de tela inicial
        self.state_manager.change_state(self.states["START_SCREEN"], self)
        
        # Carregar texturas dos jogadores (idle + caminhada)
        from render.texture_loader import load_texture
        self.player_textures = {
            1: load_texture("assets/textures/player1.png"),
            2: load_texture("assets/textures/player2.png")
        }
        self.player_walk_textures = {
            1: [
                load_texture("assets/textures/player1_walk1.png"),
                load_texture("assets/textures/player1_walk2.png"),
            ],
            2: [
                load_texture("assets/textures/player2_walk1.png"),
                load_texture("assets/textures/player2_walk2.png"),
            ]
        }
        self.map_textures = {
            "wall": load_texture("assets/textures/bloco_paredes.png"),
            "brick": load_texture("assets/textures/bloco_caixas.png")
        }

    def _init_opengl(self):
        # Configure glOrtho 
        glViewport(0, 0, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # Eixo Y invertido para corresponder à orientação de tela 2D padrão do Pygame (0,0 no canto superior esquerdo)
        glOrtho(0, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Configuração padrão de blending
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Desativa texturas 2D por padrão (deve ser ativado apenas para os sprites texturizados)
        glDisable(GL_TEXTURE_2D)

    def run(self):
        # Loop principal único
        while self.running:
            dt = self.clock.tick(settings.FPS) / 1000.0
            
            # Tratamento de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.state_manager.current_state.handle_event(event, self)
            
            # Atualização lógica e renderização delegadas ao estado ativo
            self.state_manager.current_state.update(dt, self)
            self.state_manager.current_state.render(self)
            
            # Único display flip do loop principal
            pygame.display.flip()
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
