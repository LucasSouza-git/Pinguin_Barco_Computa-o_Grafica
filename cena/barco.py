"""Barco a motor estilizado.

Eixos locais: proa em +X, vertical +Y, linha d'agua em y=0.
Grafo de cena:
  Barco (raiz: translacao ao longo do trajeto)
  +- pivo_oscilacao (bob vertical + roll + pitch)
     +- casco, proa, deck, cabine, vidro, teto
     +- motor -> pivo_helice -> cubo, 3 pas
     +- ponto_embarque (Object3D vazio: onde o pinguim pousa)
"""
import math

from cena.fabrica import Object3D, criar_caixa, criar_esfera, posicionar, carregar_textura
from cena.transformacoes import compor

COR_CASCO = (0.85, 0.20, 0.18)
COR_CABINE = (0.92, 0.92, 0.95)
COR_TETO = (0.15, 0.30, 0.65)
COR_VIDRO = (0.35, 0.60, 0.80)
COR_METAL = (0.30, 0.31, 0.34)

HELICE_POS = (-1.88, 0.40, 0.0)
VEL_HELICE_MAX = 38.0   # rad/s navegando
VEL_HELICE_IDLE = 6.0   # rad/s parado


class Barco(Object3D):
    def __init__(self):
        super().__init__()
        self.x = 0.0
        self.z = 0.0
        self.t_osc = 0.0
        self.ang_helice = 0.0
        self.vel_helice = VEL_HELICE_IDLE
        self.vel_helice_alvo = VEL_HELICE_IDLE

        self.pivo_oscilacao = Object3D()
        self.add(self.pivo_oscilacao)
        P = self.pivo_oscilacao

        casco = criar_caixa(3.0, 0.6, 1.4, COR_CASCO)
        posicionar(casco, (0, 0.1, 0))
        P.add(casco)

        # proa pontuda: caixa girada 45 graus (diagonal = largura do casco)
        proa = criar_caixa(0.99, 0.6, 0.99, COR_CASCO)
        posicionar(proa, (1.5, 0.1, 0), ry=math.pi / 4)
        P.add(proa)

        deck = criar_caixa(2.9, 0.05, 1.2, (1, 1, 1), textura=carregar_textura("madeira.png"),
                           repeticao=(2, 1))
        posicionar(deck, (-0.05, 0.425, 0))
        P.add(deck)

        cabine = criar_caixa(0.9, 0.7, 1.0, COR_CABINE)
        posicionar(cabine, (0.55, 0.8, 0))
        P.add(cabine)
        vidro = criar_caixa(0.04, 0.30, 0.76, COR_VIDRO, brilho=128, especular=0.9)
        posicionar(vidro, (1.02, 0.88, 0))
        P.add(vidro)
        teto = criar_caixa(1.05, 0.08, 1.15, COR_TETO)
        posicionar(teto, (0.55, 1.19, 0))
        P.add(teto)

        # motor de popa estilizado, com helice exposta (visivel acima da agua)
        motor = criar_caixa(0.30, 0.55, 0.40, COR_METAL)
        posicionar(motor, (-1.65, 0.62, 0))
        P.add(motor)

        self.pivo_helice = Object3D()
        posicionar(self.pivo_helice, HELICE_POS)
        P.add(self.pivo_helice)
        self.pivo_helice.add(posicionar(criar_esfera(0.08, COR_METAL), (0, 0, 0)))
        for k in range(3):
            pa = Object3D()
            posicionar(pa, rx=k * 2.0 * math.pi / 3.0)       # rotacao de cada pa
            malha = criar_caixa(0.03, 0.30, 0.10, (0.85, 0.85, 0.2))
            posicionar(malha, (0, 0.17, 0))                  # translada para fora do eixo
            pa.add(malha)
            self.pivo_helice.add(pa)

        # ponto onde o pinguim pousa/fica (area livre do deck)
        self.ponto_embarque = Object3D()
        posicionar(self.ponto_embarque, (-0.6, 0.45, 0))
        P.add(self.ponto_embarque)

        self.aplicar()

    def aplicar(self):
        """Grava a posicao ao longo do trajeto + oscilacao + giro da helice."""
        t = self.t_osc
        bob = 0.04 * math.sin(1.6 * t)
        roll = 0.035 * math.sin(1.1 * t + 1.0)     # em torno do eixo da proa (X)
        pitch = 0.020 * math.sin(1.3 * t)          # em torno de Z
        self.transform = compor((self.x, 0.0, self.z))
        self.pivo_oscilacao.transform = compor((0, bob, 0), rx=roll, rz=pitch)
        self.pivo_helice.transform = compor(HELICE_POS, rx=self.ang_helice)

    def avancar(self, dt):
        """Avanca oscilacao e helice. dt = tempo decorrido (0 quando pausado)."""
        self.t_osc += dt
        self.vel_helice += (self.vel_helice_alvo - self.vel_helice) * min(1.0, 3.0 * dt)
        self.ang_helice += self.vel_helice * dt
        self.aplicar()
