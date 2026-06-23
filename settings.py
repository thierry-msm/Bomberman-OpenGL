# Configurações globais do jogo Bomberman 2D OpenGL

# Resolução da tela e Grid
TILE_SIZE = 64
GRID_COLS = 13
GRID_ROWS = 11
HUD_HEIGHT = 64

SCREEN_WIDTH = GRID_COLS * TILE_SIZE    # 13 * 64 = 832
SCREEN_HEIGHT = (GRID_ROWS * TILE_SIZE) + HUD_HEIGHT  # 11 * 64 + 64 = 768

# Frame Rate
FPS = 60

# Cores normalizadas para OpenGL (escala de 0.0 a 1.0)
COLOR_CLEAR_START = (0.1, 0.1, 0.2, 1.0)      # Azul escuro
COLOR_CLEAR_PLAYING = (0.1, 0.5, 0.1, 1.0)    # Verde grama
COLOR_CLEAR_SCORE = (0.2, 0.1, 0.1, 1.0)      # Marrom escuro
COLOR_CLEAR_OVER = (0.4, 0.1, 0.1, 1.0)       # Vermelho escuro

# Cores genéricas para textos e overlays
COLOR_WHITE = (1.0, 1.0, 1.0, 1.0)
COLOR_BLACK = (0.0, 0.0, 0.0, 1.0)
COLOR_YELLOW = (1.0, 1.0, 0.0, 1.0)
COLOR_RED = (1.0, 0.0, 0.0, 1.0)
COLOR_GREEN = (0.0, 1.0, 0.0, 1.0)
COLOR_GRAY = (0.5, 0.5, 0.5, 1.0)
