import pygame

# Mapeamentos de teclas contínuas de movimentação
P1_MOVEMENT_KEYS = {
    "up": pygame.K_w,
    "down": pygame.K_s,
    "left": pygame.K_a,
    "right": pygame.K_d
}

P2_MOVEMENT_KEYS = {
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT
}

def get_movement_direction(pressed_keys, player_id):
    """
    Analisa o estado atual do teclado e retorna a direção (dx, dy) normalizada para o jogador.
    """
    keys = P1_MOVEMENT_KEYS if player_id == 1 else P2_MOVEMENT_KEYS
    dx, dy = 0, 0
    
    if pressed_keys[keys["left"]]:
        dx -= 1
    if pressed_keys[keys["right"]]:
        dx += 1
    if pressed_keys[keys["up"]]:
        dy -= 1
    if pressed_keys[keys["down"]]:
        dy += 1
        
    # Se houver movimentação diagonal, normalizamos para que a velocidade não aumente
    # Neste jogo 2D simples, podemos ou normalizar ou aceitar dx/dy direto.
    # Vamos retornar dx, dy normalizados se não forem zero.
    if dx != 0 and dy != 0:
        # Fator de normalização simples para diagonal: 1 / sqrt(2) ~ 0.7071
        return dx * 0.7071, dy * 0.7071
    return float(dx), float(dy)
