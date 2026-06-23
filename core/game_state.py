import random
import pygame
from entities.tilemap import TileMap
from entities.player import Player
from entities.bomb import Bomb
from entities.explosion import Explosion
from entities.powerup import PowerUp
import core.collision as collision
import core.input_handler as input_handler

class GameState:
    """Mantém e atualiza o estado dinâmico da rodada atual do jogo."""
    
    def __init__(self):
        # 1. Mapa em Grade
        self.tilemap = TileMap()
        
        # 2. Jogadores (Posições iniciais nos cantos livres)
        self.players = {
            1: Player(id=1, col=1.0, row=1.0, speed=4.0, bomb_limit=1, bomb_range=2, alive=True),
            2: Player(id=2, col=11.0, row=9.0, speed=4.0, bomb_limit=1, bomb_range=2, alive=True)
        }
        
        self.bombs = []
        self.explosions = []
        self.powerups = []

    def update(self, dt, pressed_keys):
        """Atualiza a lógica física, inputs e timers da rodada."""
        # 1. Atualizar movimentação dos jogadores
        for player_id, player in self.players.items():
            if not player.alive:
                continue
                
            dx, dy = input_handler.get_movement_direction(pressed_keys, player_id)
            if dx != 0.0 or dy != 0.0:
                # Calcula deslocamento pretendido
                d_col = dx * player.speed * dt
                d_row = dy * player.speed * dt
                
                # Deslizamento: tenta mover no eixo X, depois no eixo Y de forma independente
                # Eixo X
                new_col = player.col + d_col
                if not (collision.collides_with_map(new_col, player.row, self.tilemap) or
                        collision.collides_with_bombs(new_col, player.row, player, self.bombs)):
                    player.col = new_col
                
                # Eixo Y
                new_row = player.row + d_row
                if not (collision.collides_with_map(player.col, new_row, self.tilemap) or
                        collision.collides_with_bombs(player.col, new_row, player, self.bombs)):
                    player.row = new_row

        # 2. Atualizar estado do Bomb Trap (verificar se os donos já saíram do tile de suas bombas)
        collision.check_all_bombs_trap_exit(self.players, self.bombs)

        # 3. Atualizar Temporizadores das Bombas
        bombs_to_detonate = []
        for bomb in self.bombs:
            bomb.timer -= dt
            if bomb.timer <= 0.0:
                bombs_to_detonate.append(bomb)
                
        # Detonar as bombas expiradas
        for bomb in bombs_to_detonate:
            # Pode ocorrer de uma bomba já ter sido detonada por reação em cadeia
            if bomb in self.bombs:
                self.detonate_bomb(bomb)

        # 4. Atualizar Temporizadores das Explosões
        active_explosions = []
        for explosion in self.explosions:
            explosion.timer -= dt
            if explosion.timer > 0.0:
                active_explosions.append(explosion)
        self.explosions = active_explosions

        # 5. Colisão dos Jogadores com Explosões (Morte)
        for player in self.players.values():
            if player.alive:
                if collision.check_player_explosion_collision(player, self.explosions):
                    player.alive = False
                    print(f"[GameState] Jogador {player.id} foi eliminado!")

        # 6. Colisão dos Jogadores com Power-ups
        for player in self.players.values():
            if player.alive:
                pickups = collision.check_powerup_pickup(player, self.powerups)
                for p in pickups:
                    self.apply_powerup(player, p)
                    self.powerups.remove(p)

    def plant_bomb(self, player_id):
        """Tenta plantar uma bomba na célula atual onde o jogador está."""
        player = self.players.get(player_id)
        if not player or not player.alive:
            return
            
        # Calcula a célula do grid mais próxima do jogador
        grid_col = int(player.col + 0.5)
        grid_row = int(player.row + 0.5)
        
        # 1. Verificar limite de bombas do jogador na tela
        active_bombs = sum(1 for b in self.bombs if b.owner_id == player_id)
        if active_bombs >= player.bomb_limit:
            return
            
        # 2. Verificar se já existe uma bomba nesta célula
        for b in self.bombs:
            if b.col == grid_col and b.row == grid_row:
                return # Já existe bomba
                
        # 3. Criar nova bomba
        new_bomb = Bomb(
            col=grid_col,
            row=grid_row,
            owner_id=player_id,
            timer=3.0,
            bomb_range=player.bomb_range,
            collision_locked=False
        )
        self.bombs.append(new_bomb)
        print(f"[GameState] Jogador {player_id} plantou bomba em ({grid_col}, {grid_row}).")

    def detonate_bomb(self, bomb):
        """Executa a detonação de uma bomba e calcula a propagação da explosão em cruz."""
        if bomb in self.bombs:
            self.bombs.remove(bomb)
            
        explosion_tiles = [(bomb.col, bomb.row)]
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)] # Cima, Baixo, Esquerda, Direita
        
        for dc, dr in directions:
            for step in range(1, bomb.bomb_range + 1):
                tc = bomb.col + dc * step
                tr = bomb.row + dr * step
                
                # Tipo de bloco na posição alvo
                tile_type = self.tilemap.get_tile(tc, tr)
                
                # Se colidir com bloco indestrutível, a propagação para imediatamente
                if tile_type == TileMap.TILE_WALL:
                    break
                    
                # Se for um bloco destrutível (tijolo), quebra, pode gerar power-up e para
                if tile_type == TileMap.TILE_BRICK:
                    explosion_tiles.append((tc, tr))
                    self.tilemap.set_tile(tc, tr, TileMap.TILE_EMPTY)
                    self.spawn_powerup_chance(tc, tr)
                    break
                    
                # Se encontrar outra bomba, engatilha reação em cadeia imediata
                bomb_found = None
                for b in self.bombs:
                    if b.col == tc and b.row == tr:
                        bomb_found = b
                        break
                if bomb_found:
                    explosion_tiles.append((tc, tr))
                    # Força detonação definindo timer para zero (será processada logo a seguir)
                    bomb_found.timer = -0.01
                    break
                    
                # Se for caminho livre, continua propagação
                if tile_type == TileMap.TILE_EMPTY:
                    explosion_tiles.append((tc, tr))
                    # Destruir power-ups que estejam no caminho da explosão
                    p_to_remove = [p for p in self.powerups if p.col == tc and p.row == tr]
                    for p in p_to_remove:
                        self.powerups.remove(p)

        # Adiciona a explosão gerada à lista
        self.explosions.append(Explosion(tiles=explosion_tiles, timer=0.5, light_radius=2.5))
        print(f"[GameState] Bomba detonada em ({bomb.col}, {bomb.row}). Explosão gerada em {len(explosion_tiles)} tiles.")

    def spawn_powerup_chance(self, col, row):
        """Tenta spawnar um powerup aleatório ao destruir um bloco (25% de chance)."""
        if random.random() < 0.25:
            pu_type = random.choice(["bomb_limit", "bomb_range", "speed"])
            new_pu = PowerUp(col=col, row=row, type=pu_type)
            self.powerups.append(new_pu)
            print(f"[GameState] Power-up '{pu_type}' surgiu em ({col}, {row}).")

    def apply_powerup(self, player, powerup):
        """Aplica o efeito do powerup ao jogador correspondente."""
        if powerup.type == "bomb_limit":
            player.bomb_limit += 1
            print(f"[PowerUp] P{player.id} coletou +1 limite de bombas (Total: {player.bomb_limit}).")
        elif powerup.type == "bomb_range":
            player.bomb_range += 1
            print(f"[PowerUp] P{player.id} coletou +1 alcance de explosão (Total: {player.bomb_range}).")
        elif powerup.type == "speed":
            player.speed += 0.5
            print(f"[PowerUp] P{player.id} coletou +0.5 de velocidade (Total: {player.speed:.1f}).")
