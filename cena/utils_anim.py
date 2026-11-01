"""Funcoes puras de animacao (sem dependencia do framework).

Todas operam sobre um parametro normalizado t em [0, 1], que o Diretor
calcula a partir do TEMPO DECORRIDO (dt acumulado), nunca de contagem de quadros.
"""
import math
import numpy as np


def limitar(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_vec(p0, p1, t):
    return np.asarray(p0, float) + (np.asarray(p1, float) - np.asarray(p0, float)) * t


def ease_in_out(t):
    """Smoothstep: acelera e desacelera suavemente."""
    t = limitar(t)
    return t * t * (3.0 - 2.0 * t)


def ease_out(t):
    """Desaceleracao (usada na chegada do barco)."""
    t = limitar(t)
    return 1.0 - (1.0 - t) ** 3


def ease_in(t):
    """Aceleracao (usada na saida do barco)."""
    t = limitar(t)
    return t ** 3


def parabola(p0, p1, altura, t):
    """Arco de salto: interpolacao linear de p0 a p1 + elevacao 4*h*t*(1-t)."""
    t = limitar(t)
    p = lerp_vec(p0, p1, t)
    p[1] += 4.0 * altura * t * (1.0 - t)
    return p


def lerp_angulo(a, b, t):
    """Interpola angulos (rad) pelo caminho mais curto."""
    d = (b - a + math.pi) % (2.0 * math.pi) - math.pi
    return a + d * t


def perfil_helice(u, sobe=0.1, desce=0.3):
    """Fator 0..1 da rotacao da helice ao longo de um trajeto (rampa de subida e descida)."""
    u = limitar(u)
    f = 1.0
    if sobe > 0 and u < sobe:
        f = u / sobe
    if desce > 0 and u > 1.0 - desce:
        f = min(f, (1.0 - u) / desce)
    return f
