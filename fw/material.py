"""Texture e Material (Phong: ambiente + difusa + especular)."""
import numpy as np
import pygame
from OpenGL.GL import (glGenTextures, glBindTexture, glTexImage2D, glTexParameteri, glGenerateMipmap,
                       GL_TEXTURE_2D, GL_RGBA, GL_UNSIGNED_BYTE, GL_TEXTURE_MIN_FILTER,
                       GL_TEXTURE_MAG_FILTER, GL_LINEAR, GL_LINEAR_MIPMAP_LINEAR, GL_TEXTURE_WRAP_S,
                       GL_TEXTURE_WRAP_T, GL_REPEAT)


class Texture:
    """Imagem -> textura 2D com mipmaps e repeticao (GL_REPEAT)."""
    def __init__(self, caminho):
        img = pygame.image.load(caminho)
        w, h = img.get_size()
        dados = pygame.image.tostring(img.convert_alpha(), "RGBA", True)   # True: origem UV embaixo
        self.id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, dados)
        glGenerateMipmap(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)


class Material:
    def __init__(self, cor=(1, 1, 1), textura=None, brilho=32.0, especular=0.3, repeticao=(1, 1)):
        self.cor = np.array(cor, float)
        self.textura = textura
        self.brilho = float(brilho)
        self.especular = float(especular)
        self.repeticao = np.array(repeticao if repeticao is not None else (1, 1), float)
