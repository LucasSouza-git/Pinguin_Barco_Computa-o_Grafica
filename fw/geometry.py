"""Geometrias por composicao de formas: caixa, esfera, cilindro e retangulo.

Layout do vertice (intercalado): posicao(3) | normal(3) | uv(2)  -> atributos 0, 1 e 2
do vertex shader (vertexPosition, vertexNormal, vertexUV).
"""
import math
import numpy as np
from OpenGL.GL import (glGenVertexArrays, glBindVertexArray, glGenBuffers, glBindBuffer,
                       glBufferData, glEnableVertexAttribArray, glVertexAttribPointer,
                       glDrawArrays, GL_ARRAY_BUFFER, GL_STATIC_DRAW, GL_FLOAT, GL_FALSE,
                       GL_TRIANGLES)
import ctypes


class Geometry:
    def __init__(self, pos, nor, uv):
        self.pos = np.asarray(pos, np.float32).reshape(-1, 3)
        self.nor = np.asarray(nor, np.float32).reshape(-1, 3)
        self.uv = np.asarray(uv, np.float32).reshape(-1, 2)
        self.vao = None

    def escalar(self, sx, sy, sz):
        """Escala vertices; normais transformadas pela inversa transposta (divide por s)."""
        s = np.array([sx, sy, sz], np.float32)
        self.pos = self.pos * s
        n = self.nor / s
        self.nor = (n / np.linalg.norm(n, axis=1, keepdims=True)).astype(np.float32)

    def _enviar(self):
        dados = np.hstack([self.pos, self.nor, self.uv]).astype(np.float32)
        self.n_vertices = len(dados)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, dados.nbytes, dados, GL_STATIC_DRAW)
        passo = 8 * 4
        for loc, n, off in ((0, 3, 0), (1, 3, 12), (2, 2, 24)):
            glEnableVertexAttribArray(loc)
            glVertexAttribPointer(loc, n, GL_FLOAT, GL_FALSE, passo, ctypes.c_void_p(off))

    def desenhar(self):
        if self.vao is None:
            self._enviar()
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, self.n_vertices)


def _quad(p, n, uv=((0, 0), (1, 0), (1, 1), (0, 1))):
    """Dois triangulos (anti-horario visto de fora) a partir de 4 cantos."""
    idx = (0, 1, 2, 0, 2, 3)
    return [p[i] for i in idx], [n] * 6, [uv[i] for i in idx]


def caixa(l, a, p):
    x, y, z = l / 2, a / 2, p / 2
    faces = [  # (4 cantos em sentido anti-horario visto de fora, normal)
        ([(-x, -y, z), (x, -y, z), (x, y, z), (-x, y, z)], (0, 0, 1)),
        ([(x, -y, -z), (-x, -y, -z), (-x, y, -z), (x, y, -z)], (0, 0, -1)),
        ([(x, -y, z), (x, -y, -z), (x, y, -z), (x, y, z)], (1, 0, 0)),
        ([(-x, -y, -z), (-x, -y, z), (-x, y, z), (-x, y, -z)], (-1, 0, 0)),
        ([(-x, y, z), (x, y, z), (x, y, -z), (-x, y, -z)], (0, 1, 0)),
        ([(-x, -y, -z), (x, -y, -z), (x, -y, z), (-x, -y, z)], (0, -1, 0)),
    ]
    P, N, UV = [], [], []
    for cantos, n in faces:
        a_, b_, c_ = _quad(cantos, n)
        P += a_; N += b_; UV += c_
    return Geometry(P, N, UV)


def esfera(r, seg=32, alt=16):
    def ponto(i, j):
        th, ph = math.pi * i / alt, 2 * math.pi * j / seg
        n = (math.sin(th) * math.cos(ph), math.cos(th), math.sin(th) * math.sin(ph))
        return n, (j / seg, 1 - i / alt)
    P, N, UV = [], [], []
    for i in range(alt):
        for j in range(seg):
            q = [ponto(i, j), ponto(i + 1, j), ponto(i + 1, j + 1), ponto(i, j + 1)]
            for k in (0, 2, 1, 0, 3, 2):   # ordem anti-horaria vista de fora
                n, uv = q[k]
                P.append(tuple(r * c for c in n)); N.append(n); UV.append(uv)
    return Geometry(P, N, UV)


def cilindro(r, h, seg=24):
    P, N, UV = [], [], []
    y0, y1 = -h / 2, h / 2
    for j in range(seg):
        a0, a1 = 2 * math.pi * j / seg, 2 * math.pi * (j + 1) / seg
        c0, s0, c1, s1 = math.cos(a0), math.sin(a0), math.cos(a1), math.sin(a1)
        q = [(r * c0, y0, -r * s0), (r * c1, y0, -r * s1), (r * c1, y1, -r * s1), (r * c0, y1, -r * s0)]
        nn = [(c0, 0, -s0), (c1, 0, -s1), (c1, 0, -s1), (c0, 0, -s0)]
        uvs = [(j / seg, 0), ((j + 1) / seg, 0), ((j + 1) / seg, 1), (j / seg, 1)]
        for k in (0, 1, 2, 0, 2, 3):
            P.append(q[k]); N.append(nn[k]); UV.append(uvs[k])
        for y, ny, ordem in ((y1, 1, (0, 1, 2)), (y0, -1, (0, 2, 1))):   # tampas
            tri = [(0, y, 0), (r * c0, y, -r * s0), (r * c1, y, -r * s1)]
            for k in ordem:
                P.append(tri[k]); N.append((0, ny, 0)); UV.append((0.5 + 0.5 * tri[k][0] / r, 0.5 - 0.5 * tri[k][2] / r))
    # a ordem das tampas foi escolhida para a face externa ficar anti-horaria
    return Geometry(P, N, UV)


def retangulo(l, a):
    x, y = l / 2, a / 2
    p, n, uv = _quad([(-x, -y, 0), (x, -y, 0), (x, y, 0), (-x, y, 0)], (0, 0, 1))
    return Geometry(p, n, uv)
