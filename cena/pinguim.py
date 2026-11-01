"""Pinguim: modelo hierarquico + animacao procedural controlada por tempo.

Eixos locais: o pinguim olha para +Z; origem nos pes (y=0).
Grafo de cena:
  Pinguim (raiz: posicao/giro)
  +- pivo_corpo (balanco, inclinacao, squash/stretch)
     +- corpo, barriga
     +- pivo_cabeca -> cabeca, bico, olhos
     +- pivo_nad_esq -> nadadeira   (ombro: giro em Z)
     +- pivo_nad_dir -> nadadeira
     +- pes
"""
import math
import numpy as np

from cena.fabrica import Object3D, criar_caixa, criar_esfera, posicionar
from cena.transformacoes import compor, matriz_mundo, extrair_pos_yaw

PRETO = (0.08, 0.09, 0.14)
BRANCO = (0.95, 0.95, 0.97)
LARANJA = (0.95, 0.55, 0.10)

MODOS = ("idle", "acenar", "andar", "pular", "comemorar")


class Pinguim(Object3D):
    def __init__(self):
        super().__init__()
        # estado de pose da raiz (o Diretor escreve aqui; avancar() grava na matriz)
        self.pos = np.zeros(3)
        self.yaw = 0.0
        self.modo = "idle"
        self.t_anim = 0.0

        self.pivo_corpo = Object3D()
        self.add(self.pivo_corpo)

        corpo = criar_esfera(0.40, PRETO, escala=(0.85, 1.25, 0.80))
        posicionar(corpo, (0, 0.55, 0))
        self.pivo_corpo.add(corpo)

        barriga = criar_esfera(0.36, BRANCO, escala=(0.78, 1.15, 0.60))
        posicionar(barriga, (0, 0.52, 0.15))
        self.pivo_corpo.add(barriga)

        # cabeca
        self.pivo_cabeca = Object3D()
        posicionar(self.pivo_cabeca, (0, 1.12, 0))
        self.pivo_corpo.add(self.pivo_cabeca)
        cabeca = criar_esfera(0.27, PRETO)
        posicionar(cabeca, (0, 0.12, 0))
        self.pivo_cabeca.add(cabeca)
        bico = criar_esfera(0.10, LARANJA, escala=(1.0, 0.6, 1.7))
        posicionar(bico, (0, 0.09, 0.27))
        self.pivo_cabeca.add(bico)
        for lado in (-1, 1):
            olho = criar_esfera(0.055, BRANCO)
            posicionar(olho, (0.10 * lado, 0.20, 0.215))
            self.pivo_cabeca.add(olho)
            pupila = criar_esfera(0.03, (0, 0, 0))
            posicionar(pupila, (0.10 * lado, 0.20, 0.255))
            self.pivo_cabeca.add(pupila)

        # nadadeiras: pivo no ombro, malha pendurada para baixo
        self.pivo_nad_esq = Object3D()  # lado +X
        self.pivo_nad_dir = Object3D()  # lado -X
        for pivo, lado in ((self.pivo_nad_esq, 1), (self.pivo_nad_dir, -1)):
            posicionar(pivo, (0.36 * lado, 0.85, 0))
            nad = criar_caixa(0.07, 0.50, 0.20, PRETO)
            posicionar(nad, (0.03 * lado, -0.24, 0))
            pivo.add(nad)
            self.pivo_corpo.add(pivo)

        # pes
        for lado in (-1, 1):
            pe = criar_esfera(0.10, LARANJA, escala=(1.0, 0.4, 1.7))
            posicionar(pe, (0.15 * lado, 0.04, 0.12))
            self.add(pe)

        self.aplicar()

    # ------------------------------------------------------------------ pose
    def aplicar(self):
        self.transform = compor(self.pos, ry=self.yaw)

    def avancar(self, dt):
        """Avanca a animacao do modo atual. dt = tempo decorrido (0 quando pausado)."""
        self.t_anim += dt
        w = self.t_anim
        esq = dir_ = 0.15           # angulo das nadadeiras (rad, + = para fora)
        roll = pitch = bounce = 0.0
        head_yaw = 0.0
        sy = 1.0

        if self.modo == "idle":
            esq = dir_ = 0.15 + 0.05 * math.sin(2.0 * w)
            roll = 0.02 * math.sin(1.5 * w)
            head_yaw = 0.25 * math.sin(0.8 * w)
        elif self.modo == "acenar":      # chamado: nadadeira esquerda sobe e balanca
            esq = 2.4 + 0.45 * math.sin(9.0 * w)
            dir_ = 0.20
            head_yaw = 0.12 * math.sin(4.5 * w)
        elif self.modo == "andar":       # gingado de pinguim
            ciclo = 9.0 * w
            roll = 0.14 * math.sin(ciclo)
            bounce = 0.03 * abs(math.sin(ciclo))
            esq = 0.35 + 0.25 * math.sin(ciclo)
            dir_ = 0.35 - 0.25 * math.sin(ciclo)
        elif self.modo == "pular":       # nadadeiras abertas, corpo inclinado
            esq = dir_ = 1.1
            pitch = 0.25
        elif self.modo == "comemorar":
            esq = dir_ = 2.6 + 0.35 * math.sin(10.0 * w)
            sy = 1.0 + 0.06 * math.sin(10.0 * w)   # squash & stretch (escala)
            bounce = 0.04 * abs(math.sin(5.0 * w))

        self.pivo_corpo.transform = compor((0, bounce, 0), rx=pitch, rz=roll, escala=(1, sy, 1))
        self.pivo_cabeca.transform = compor((0, 1.12, 0), ry=head_yaw)
        self.pivo_nad_esq.transform = compor((0.36, 0.85, 0), rz=esq)
        self.pivo_nad_dir.transform = compor((-0.36, 0.85, 0), rz=-dir_)
        self.aplicar()

    # ------------------------------------------------------- grafo de cena
    def anexar_a(self, novo_pai):
        """Troca o pai preservando a posicao/orientacao NO MUNDO (sem 'pulo' visual).

        local_novo = inversa(mundo_do_novo_pai) @ mundo_atual
        """
        mundo = matriz_mundo(self)
        if self.parent is not None:
            self.parent.remove(self)
        novo_pai.add(self)
        local = np.linalg.inv(matriz_mundo(novo_pai)) @ mundo
        self.pos, self.yaw = extrair_pos_yaw(local)
        self.aplicar()
