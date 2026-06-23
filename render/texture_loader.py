# Carregador de Texturas via Pillow para OpenGL

from PIL import Image
from OpenGL.GL import *


def load_texture(filepath):
    """
    Carrega uma imagem do disco usando Pillow, converte para RGBA,
    aplica flip vertical e envia ao OpenGL como textura 2D.
    
    Usa GL_NEAREST como filtro para preservar a nitidez de pixel-art.
    Retorna o ID da textura OpenGL gerada.
    """
    try:
        img = Image.open(filepath)
    except FileNotFoundError:
        print(f"[TextureLoader] Arquivo não encontrado: {filepath}")
        return None
    except Exception as e:
        print(f"[TextureLoader] Erro ao abrir imagem {filepath}: {e}")
        return None

    # Converter para RGBA (garante canal alpha)
    img = img.convert("RGBA")

    # Flip vertical — OpenGL espera a origem no canto inferior esquerdo
    img = img.transpose(Image.FLIP_TOP_BOTTOM)

    width, height = img.size
    data = img.tobytes()

    # Gerar textura OpenGL
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    # Filtro GL_NEAREST para visual pixel-art nítido (sem suavização)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    # Enviar dados da imagem para a GPU
    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGBA,
        width, height, 0,
        GL_RGBA, GL_UNSIGNED_BYTE, data
    )

    print(f"[TextureLoader] Textura carregada: {filepath} ({width}x{height}) -> ID {texture_id}")
    return texture_id


def draw_textured_quad(texture_id, x, y, w, h):
    """
    Desenha um quad texturizado na posição (x, y) com dimensões (w, h).
    Assume que GL_TEXTURE_2D já está habilitado pelo chamador.
    """
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glColor4f(1.0, 1.0, 1.0, 1.0)

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 1.0); glVertex2f(x, y)
    glTexCoord2f(1.0, 1.0); glVertex2f(x + w, y)
    glTexCoord2f(1.0, 0.0); glVertex2f(x + w, y + h)
    glTexCoord2f(0.0, 0.0); glVertex2f(x, y + h)
    glEnd()
