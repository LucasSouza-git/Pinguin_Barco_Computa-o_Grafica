"""Matrizes 4x4 e utilidades de grafo de cena (as matrizes base ficam em fw/matrix.py)."""
import math
from fw.matrix import compor, _rx, _ry, _rz  # noqa: F401


def matriz_mundo(obj):
    """Matriz local -> mundo, percorrendo a cadeia de pais (grafo de cena)."""
    m = obj.transform
    p = obj.parent
    while p is not None:
        m = p.transform @ m
        p = p.parent
    return m


def posicao_mundo(obj):
    return matriz_mundo(obj)[:3, 3].copy()


def extrair_pos_yaw(m):
    """Posicao e angulo de giro em Y de uma matriz sem escala."""
    return m[:3, 3].copy(), math.atan2(m[0, 2], m[2, 2])
