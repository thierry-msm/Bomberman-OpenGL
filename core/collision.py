# Módulo de Tratamento de Colisões do Jogo

def get_player_bbox(player_col, player_row, size=0.7):
    """
    Retorna a caixa delimitadora (left, right, top, bottom) do jogador no grid.
    Com o tamanho padrão de 0.7, o jogador é ligeiramente menor que 1.0,
    centralizado na célula, facilitando a movimentação e o deslizamento em corredores.
    """
    offset = (1.0 - size) / 2.0
    return (
        player_col + offset,                  # left
        player_col + 1.0 - offset,            # right
        player_row + offset,                  # top
        player_row + 1.0 - offset             # bottom
    )


def collides_with_map(col, row, tilemap, size=0.7):
    """Verifica se o jogador na posição (col, row) colide com alguma parede ou tijolo do mapa."""
    left, right, top, bottom = get_player_bbox(col, row, size)
    
    # Índices dos tiles sobrepostos
    min_col = int(left)
    max_col = int(right)
    min_row = int(top)
    max_row = int(bottom)
    
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            if not tilemap.is_walkable(c, r):
                return True
    return False


def collides_with_bombs(col, row, player, bombs, size=0.7):
    """Verifica se o jogador colide com alguma bomba sólida no mapa (respeitando o bomb trap)."""
    left, right, top, bottom = get_player_bbox(col, row, size)
    
    for bomb in bombs:
        # Limites da célula da bomba
        b_left = bomb.col
        b_right = bomb.col + 1.0
        b_top = bomb.row
        b_bottom = bomb.row + 1.0
        
        # Verifica sobreposição de AABB
        overlap = (left < b_right) and (right > b_left) and (top < b_bottom) and (bottom > b_top)
        if overlap:
            # Se for outro jogador, ou se a bomba já travou colisão para o dono, bloqueia
            if player.id != bomb.owner_id or bomb.collision_locked:
                return True
    return False


def check_bomb_trap_exit(player, bomb, size=0.7):
    """
    Implementa a regra de escape da bomba recém-plantada (Bomb Trap).
    Verifica se o dono da bomba já saiu completamente da célula dela.
    Em caso positivo, trava a colisão definitiva para impedir reentrada.
    """
    if bomb.collision_locked:
        return

    if player.id == bomb.owner_id:
        left, right, top, bottom = get_player_bbox(player.col, player.row, size)
        
        # Limites do tile da bomba
        b_left = bomb.col
        b_right = bomb.col + 1.0
        b_top = bomb.row
        b_bottom = bomb.row + 1.0
        
        # Verifica se ainda há qualquer sobreposição
        overlap = (left < b_right) and (right > b_left) and (top < b_top + 1.0) and (bottom > b_top)
        # Correção da condição do overlap vertical
        overlap = (left < b_right) and (right > b_left) and (top < b_bottom) and (bottom > b_top)
        
        if not overlap:
            bomb.collision_locked = True
            print(f"[BombTrap] Bomba em ({bomb.col}, {bomb.row}) agora bloqueia o dono P{player.id}.")


def check_all_bombs_trap_exit(players, bombs, size=0.7):
    """Atualiza o estado de trancamento de colisão de todas as bombas na arena."""
    for bomb in bombs:
        if not bomb.collision_locked:
            owner = players.get(bomb.owner_id)
            if owner:
                check_bomb_trap_exit(owner, bomb, size)


def check_player_explosion_collision(player, explosions, size=0.7):
    """Retorna True se o jogador estiver sobreposto a algum tile em chamas/explosão."""
    left, right, top, bottom = get_player_bbox(player.col, player.row, size)
    
    for explosion in explosions:
        for tile in explosion.tiles:
            e_col, e_row = tile
            # Sobreposição com o tile da explosão
            overlap = (left < e_col + 1.0) and (right > e_col) and (top < e_row + 1.0) and (bottom > e_row)
            if overlap:
                return True
    return False


def check_powerup_pickup(player, powerups, size=0.7):
    """Retorna a lista de power-ups que o jogador colidiu para consumo."""
    left, right, top, bottom = get_player_bbox(player.col, player.row, size)
    picked = []
    
    for p in powerups:
        overlap = (left < p.col + 1.0) and (right > p.col) and (top < p.row + 1.0) and (bottom > p.row)
        if overlap:
            picked.append(p)
            
    return picked
