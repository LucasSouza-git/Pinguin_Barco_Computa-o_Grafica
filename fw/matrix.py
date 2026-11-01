"""Matrizes 4x4 de translacao, rotacao e escala.

Convencao do framework do livro: matrizes numpy 4x4, vetores coluna,
transform_local = T * Ry * Rx * Rz * S.
"""
import math
import numpy as np


def _rx(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]], float)


def _ry(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]], float)


def _rz(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], float)


def compor(pos=(0, 0, 0), rx=0.0, ry=0.0, rz=0.0, escala=(1, 1, 1)):
    """Monta T * Ry * Rx * Rz * S (escala aceita numero ou tupla)."""
    if np.isscalar(escala):
        escala = (escala, escala, escala)
    t = np.eye(4)
    t[:3, 3] = pos
    s = np.diag([escala[0], escala[1], escala[2], 1.0])
    return t @ _ry(ry) @ _rx(rx) @ _rz(rz) @ s


