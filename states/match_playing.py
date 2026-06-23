import pygame
from OpenGL.GL import *
from state_manager import BaseState
import settings
from render.hud_renderer import draw_hud
from core.game_state import GameState
from core.round_manager import check_round_end

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
        # 1. Limpar fundo da tela com a cor padrão de gameplay
        r, g, b, a = settings.COLOR_CLEAR_PLAYING
        glClearColor(r, g, b, a)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Desativa texturas por padrão para desenhos geométricos puros
        glDisable(GL_TEXTURE_2D)
        
        # Ajudante para desenhar quadrados sólidos
        def draw_solid_quad(x, y, w, h, color):
            glColor4f(color[0], color[1], color[2], color[3])
            glBegin(GL_QUADS)
            glVertex2f(x, y)
            glVertex2f(x + w, y)
            glVertex2f(x + w, y + h)
            glVertex2f(x, y + h)
            glEnd()
            
        # 2. Renderizar Grade do Mapa (Paredes Fixas e Blocos Destrutíveis)
        tilemap = game.game_state.tilemap
        for row_idx in range(tilemap.rows):
            for col_idx in range(tilemap.cols):
                tile_type = tilemap.get_tile(col_idx, row_idx)
                x_pos = col_idx * settings.TILE_SIZE
                y_pos = settings.HUD_HEIGHT + row_idx * settings.TILE_SIZE
                
                if tile_type == 1:  # Parede Indestrutível (Cinza)
                    draw_solid_quad(x_pos, y_pos, settings.TILE_SIZE, settings.TILE_SIZE, (0.25, 0.25, 0.25, 1.0))
                    # Detalhe interno de volume
                    draw_solid_quad(x_pos + 4, y_pos + 4, settings.TILE_SIZE - 8, settings.TILE_SIZE - 8, (0.35, 0.35, 0.35, 1.0))
                elif tile_type == 2:  # Bloco Destrutível / Tijolo (Marrom)
                    draw_solid_quad(x_pos + 2, y_pos + 2, settings.TILE_SIZE - 4, settings.TILE_SIZE - 4, (0.55, 0.27, 0.07, 1.0))
                    # Detalhe de tijolo rachado
                    draw_solid_quad(x_pos + 6, y_pos + 6, settings.TILE_SIZE - 12, settings.TILE_SIZE - 12, (0.65, 0.35, 0.15, 1.0))

        # 3. Renderizar Power-ups
        for pu in game.game_state.powerups:
            x_pos = pu.col * settings.TILE_SIZE + 16
            y_pos = settings.HUD_HEIGHT + pu.row * settings.TILE_SIZE + 16
            
            # Cores diferentes para cada tipo de power-up
            if pu.type == "bomb_limit":
                pu_color = (0.9, 0.1, 0.9, 1.0)  # Magenta
            elif pu.type == "bomb_range":
                pu_color = (0.1, 0.9, 0.9, 1.0)  # Ciano
            else:
                pu_color = (0.9, 0.9, 0.1, 1.0)  # Amarelo
                
            draw_solid_quad(x_pos, y_pos, 32, 32, pu_color)
            # Centro decorativo branco
            draw_solid_quad(x_pos + 8, y_pos + 8, 16, 16, (1.0, 1.0, 1.0, 1.0))

        # 4. Renderizar Bombas
        for bomb in game.game_state.bombs:
            x_pos = bomb.col * settings.TILE_SIZE + 12
            y_pos = settings.HUD_HEIGHT + bomb.row * settings.TILE_SIZE + 12
            # Corpo da bomba (Círculo simulado por quadrado preto arredondado)
            draw_solid_quad(x_pos, y_pos, 40, 40, (0.05, 0.05, 0.05, 1.0))
            # Pavio laranja
            draw_solid_quad(x_pos + 16, y_pos - 6, 8, 8, (0.9, 0.5, 0.0, 1.0))

        # 5. Renderizar Explosões
        for explosion in game.game_state.explosions:
            for tile in explosion.tiles:
                tx, ty = tile
                x_pos = tx * settings.TILE_SIZE
                y_pos = settings.HUD_HEIGHT + ty * settings.TILE_SIZE
                # Fogo alaranjado semitransparente
                draw_solid_quad(x_pos, y_pos, settings.TILE_SIZE, settings.TILE_SIZE, (1.0, 0.35, 0.0, 0.85))
                # Centro mais quente amarelo
                draw_solid_quad(x_pos + 12, y_pos + 12, settings.TILE_SIZE - 24, settings.TILE_SIZE - 24, (1.0, 0.85, 0.1, 0.9))

        # 6. Renderizar Jogadores
        for player in game.game_state.players.values():
            if player.alive:
                # Transforma colunas/linhas flutuantes em pixels da tela
                x_pos = player.col * settings.TILE_SIZE + 8
                y_pos = settings.HUD_HEIGHT + player.row * settings.TILE_SIZE + 8
                
                # P1 é Azul, P2 é Vermelho
                p_color = (0.2, 0.6, 1.0, 1.0) if player.id == 1 else (1.0, 0.3, 0.3, 1.0)
                # Base do jogador
                draw_solid_quad(x_pos, y_pos, 48, 48, p_color)
                # Olhos decorativos brancos para destacar a face
                draw_solid_quad(x_pos + 10, y_pos + 10, 10, 10, (1.0, 1.0, 1.0, 1.0))
                draw_solid_quad(x_pos + 28, y_pos + 10, 10, 10, (1.0, 1.0, 1.0, 1.0))
                # Pupilas pretas
                draw_solid_quad(x_pos + 14, y_pos + 14, 4, 4, (0.0, 0.0, 0.0, 1.0))
                draw_solid_quad(x_pos + 32, y_pos + 14, 4, 4, (0.0, 0.0, 0.0, 1.0))

        # 7. Renderizar a HUD (por último, sobre todos os elementos e efeitos)
        draw_hud(game)
