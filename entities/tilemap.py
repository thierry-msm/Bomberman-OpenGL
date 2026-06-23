import random

class TileMap:
    """Representa a grade do mapa do Bomberman (listas de listas)."""
    
    # Constantes dos tipos de blocos
    TILE_EMPTY = 0
    TILE_WALL = 1     # Indestrutível
    TILE_BRICK = 2    # Destrutível (tijolo)

    def __init__(self, cols=13, rows=11):
        self.cols = cols
        self.rows = rows
        self.grid = self.generate_default_grid()

    def generate_default_grid(self):
        """Gera o mapa padrão do Bomberman com cantos livres para os jogadores."""
        grid = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                # 1. Bordas externas do mapa são indestrutíveis
                if r == 0 or r == self.rows - 1 or c == 0 or c == self.cols - 1:
                    row.append(self.TILE_WALL)
                # 2. Grelha interna de blocos indestrutíveis (células pares)
                elif r % 2 == 0 and c % 2 == 0:
                    row.append(self.TILE_WALL)
                # 3. Zonas livres de segurança para o Jogador 1 (canto superior esquerdo)
                elif (r == 1 and c == 1) or (r == 1 and c == 2) or (r == 2 and c == 1):
                    row.append(self.TILE_EMPTY)
                # 4. Zonas livres de segurança para o Jogador 2 (canto inferior direito)
                elif (r == self.rows - 2 and c == self.cols - 2) or \
                     (r == self.rows - 2 and c == self.cols - 3) or \
                     (r == self.rows - 3 and c == self.cols - 2):
                    row.append(self.TILE_EMPTY)
                # 5. Outros blocos podem ser destrutíveis (tijolos) ou espaços livres
                else:
                    # 60% de chance de gerar um bloco destrutível (tijolo)
                    if random.random() < 0.6:
                        row.append(self.TILE_BRICK)
                    else:
                        row.append(self.TILE_EMPTY)
            grid.append(row)
        return grid

    def get_tile(self, col, row):
        """Retorna o tipo de bloco na célula (col, row), ou TILE_WALL se fora da grade."""
        if 0 <= col < self.cols and 0 <= row < self.rows:
            return self.grid[row][col]
        return self.TILE_WALL

    def set_tile(self, col, row, value):
        """Define o tipo de bloco na célula especificada."""
        if 0 <= col < self.cols and 0 <= row < self.rows:
            self.grid[row][col] = value

    def is_walkable(self, col, row):
        """Retorna True se o bloco for livre e passável."""
        return self.get_tile(col, row) == self.TILE_EMPTY
