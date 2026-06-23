import pygame
from OpenGL.GL import *

class TextRenderer:
    """Carrega fontes do Pygame e renderiza textos como texturas OpenGL 2D."""
    
    def __init__(self):
        # Cache de fontes carregadas: (nome_da_fonte, tamanho) -> pygame.font.Font
        self._fonts = {}

    def _get_font(self, font_name, size):
        """Retorna uma fonte do cache, carregando do disco se necessário."""
        key = (font_name, size)
        if key not in self._fonts:
            try:
                # Tenta carregar uma fonte TTF se o caminho for fornecido, senão usa a padrão do sistema
                if font_name:
                    self._fonts[key] = pygame.font.Font(font_name, size)
                else:
                    self._fonts[key] = pygame.font.Font(None, size)
            except Exception as e:
                print(f"[TextRenderer] Erro ao carregar fonte {font_name}, usando SysFont: {e}")
                self._fonts[key] = pygame.font.SysFont("arial", size)
        return self._fonts[key]

    def draw_text(self, text, x, y, size=24, color=(255, 255, 255), font_name=None, align="left"):
        """Renderiza texto na posição (x, y) com o alinhamento especificado ('left', 'center', 'right')."""
        if not text:
            return

        # 1. Obter a fonte do cache
        font = self._get_font(font_name, size)
        
        # 2. Renderizar o texto em uma pygame.Surface com antialiasing
        # Para que o blend funcione corretamente no OpenGL, o fundo deve ser transparente (None)
        # pygame.Color recebe valores de 0 a 255
        pg_color = pygame.Color(int(color[0]*255), int(color[1]*255), int(color[2]*255))
        text_surface = font.render(text, True, pg_color)
        
        width = text_surface.get_width()
        height = text_surface.get_height()
        
        # Ajusta a coordenada x conforme o alinhamento solicitado
        if align == "center":
            x_pos = x - width / 2.0
        elif align == "right":
            x_pos = x - width
        else:
            x_pos = x
            
        y_pos = y

        # 3. Converter a superfície para dados brutos de pixels RGBA
        # flip=True inverte verticalmente para alinhar com a projeção invertida
        data = pygame.image.tostring(text_surface, "RGBA", True)

        # 4. Criar textura temporária OpenGL
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)

        # 5. Renderizar o quad texturizado na tela
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        
        # Define cor branca para desenhar a textura sem alterar suas cores originais
        glColor4f(1.0, 1.0, 1.0, 1.0)
        
        glBegin(GL_QUADS)
        # Mapeia os vértices considerando Y invertido do glOrtho
        glTexCoord2f(0.0, 1.0); glVertex2f(x_pos, y_pos)
        glTexCoord2f(1.0, 1.0); glVertex2f(x_pos + width, y_pos)
        glTexCoord2f(1.0, 0.0); glVertex2f(x_pos + width, y_pos + height)
        glTexCoord2f(0.0, 0.0); glVertex2f(x_pos, y_pos + height)
        glEnd()

        # 6. Desativar textura e limpar recurso da GPU para evitar vazamento de memória
        glDisable(GL_TEXTURE_2D)
        glDeleteTextures([texture_id])
