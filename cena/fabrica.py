"""ADAPTADOR entre o codigo da cena e o framework (fw/).

Todo o codigo de cena (pinguim, barco, ambiente) so conhece estas funcoes. O framework em fw/
e uma versao compacta, escrita pela dupla a partir da arquitetura do livro (STEMKOSKI; PASCALE,
2022); para trocar de framework, basta reimplementar este arquivo.
"""
import math
import os

from fw.object3d import Object3D  # noqa: F401 (reexportado para a cena)
from fw.mesh import Mesh
from fw.material import Material, Texture
from fw import geometry as geo
from fw.matrix import compor

DIR_IMAGENS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "imagens")
_cache_texturas = {}


def carregar_textura(nome_arquivo):
    """Carrega (com cache) uma imagem da pasta imagens/ como textura."""
    if nome_arquivo not in _cache_texturas:
        _cache_texturas[nome_arquivo] = Texture(os.path.join(DIR_IMAGENS, nome_arquivo))
    return _cache_texturas[nome_arquivo]


def criar_caixa(l, a, p, cor=(1, 1, 1), textura=None, repeticao=None, brilho=32, especular=0.3):
    return Mesh(geo.caixa(l, a, p), Material(cor, textura, brilho, especular, repeticao))


def criar_esfera(raio, cor=(1, 1, 1), escala=(1, 1, 1), brilho=32, especular=0.3):
    g = geo.esfera(raio)
    if tuple(escala) != (1, 1, 1):
        g.escalar(*escala)      # vertices escalados + normais corrigidas (inversa transposta)
    return Mesh(g, Material(cor, None, brilho, especular))


def criar_cilindro(raio, altura, cor=(1, 1, 1), brilho=32, especular=0.3):
    return Mesh(geo.cilindro(raio, altura), Material(cor, None, brilho, especular))


def criar_plano_horizontal(largura, profundidade, cor=(1, 1, 1), textura=None, repeticao=None,
                           pos=(0, 0, 0), brilho=64, especular=0.5):
    """Retangulo deitado no plano XZ com a normal apontando para +Y (cima)."""
    m = Mesh(geo.retangulo(largura, profundidade), Material(cor, textura, brilho, especular, repeticao),
             cast_shadow=False)
    m.transform = compor(pos=pos, rx=-math.pi / 2)   # o retangulo nasce no plano XY (normal +Z)
    return m


def posicionar(obj, pos=(0, 0, 0), rx=0.0, ry=0.0, rz=0.0, escala=(1, 1, 1)):
    """Atalho: define a transformacao local (T*Ry*Rx*Rz*S) de qualquer Object3D."""
    obj.transform = compor(pos, rx, ry, rz, escala)
    return obj
