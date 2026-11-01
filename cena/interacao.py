"""Diretor: maquina de estados que COORDENA pinguim e barco.

Regra central (requisito de interacao): cada transicao depende do OUTRO personagem.
  - o pinguim so age depois que o barco PARA;
  - o barco so parte depois que o pinguim esta EMBARCADO (filho do barco no grafo);
  - o barco so sai da doca B depois que o pinguim terminou a despedida.
Todos os tempos sao acumulados a partir de dt (segundos); pausa = dt 0.
"""
import math
from dataclasses import dataclass
from enum import Enum, auto

import numpy as np

from cena import ambiente as amb
from cena.transformacoes import posicao_mundo
from cena.utils_anim import (limitar, lerp, ease_in_out, ease_out, ease_in, lerp_angulo,
                             parabola, perfil_helice)
from cena.barco import VEL_HELICE_MAX, VEL_HELICE_IDLE


class Estado(Enum):
    ESPERA = auto()
    APROXIMACAO = auto()
    PARADA = auto()
    CHAMADO = auto()
    ATE_A_BORDA = auto()
    SALTO_EMBARQUE = auto()
    EMBARCADO = auto()
    PARTIDA = auto()
    CHEGADA = auto()
    SALTO_DESEMBARQUE = auto()
    DESPEDIDA = auto()
    SAIDA = auto()
    FIM = auto()


@dataclass
class Tempos:
    """Duracoes (s) de cada etapa; ajuste aqui o ritmo da animacao."""
    espera: float = 2.0
    aproximacao: float = 7.0
    parada: float = 1.0
    chamado: float = 2.6
    ate_a_borda: float = 1.6
    salto: float = 1.0
    embarcado: float = 2.8
    partida: float = 9.0
    chegada: float = 1.8
    despedida: float = 2.6
    saida: float = 6.0
    fim: float = 3.0
    altura_salto: float = 1.3


class Diretor:
    def __init__(self, cena, barco, pinguim, tempos=None):
        self.cena = cena
        self.barco = barco
        self.pinguim = pinguim
        self.c = tempos or Tempos()
        # o barco para com o ponto_embarque alinhado em X com o pinguim da doca
        dx = barco.ponto_embarque.transform[0, 3]
        self.x_parada_a = amb.X_DOCA_A - dx
        self.x_parada_b = amb.X_DOCA_B - dx
        self.tempo_total = 0.0
        self.historico = []          # (tempo_total, estado) - util para testes/depuracao
        self._p0 = np.zeros(3)
        self._alvo = np.zeros(3)
        self._handlers = {
            Estado.ESPERA: self._espera, Estado.APROXIMACAO: self._aproximacao,
            Estado.PARADA: self._parada, Estado.CHAMADO: self._chamado,
            Estado.ATE_A_BORDA: self._ate_a_borda, Estado.SALTO_EMBARQUE: self._salto_embarque,
            Estado.EMBARCADO: self._embarcado, Estado.PARTIDA: self._partida,
            Estado.CHEGADA: self._chegada, Estado.SALTO_DESEMBARQUE: self._salto_desembarque,
            Estado.DESPEDIDA: self._despedida, Estado.SAIDA: self._saida, Estado.FIM: self._fim,
        }
        self.reiniciar()

    # ------------------------------------------------------------ utilitarios
    def _ir(self, novo, duracao=0.0):
        """Troca de estado repassando a SOBRA de tempo do quadro (evita deriva por FPS)."""
        self.estado = novo
        self.t_estado = max(0.0, self.t_estado - duracao)
        self.historico.append((self.tempo_total, novo))

    def _pos_barco(self, x):
        self.barco.x = x
        self.barco.z = amb.Z_BARCO
        self.barco.aplicar()

    def _helice(self, fator):
        self.barco.vel_helice_alvo = lerp(VEL_HELICE_IDLE, VEL_HELICE_MAX, limitar(fator))

    def pinguim_a_bordo(self):
        return self.pinguim.parent is self.barco.ponto_embarque

    def reiniciar(self):
        """Volta ao estado inicial (usado no loop e na tecla de reinicio)."""
        if self.pinguim.parent is not self.cena:
            self.pinguim.anexar_a(self.cena)
        self.pinguim.pos = np.array([amb.X_DOCA_A, amb.Y_DOCA, amb.Z_PINGUIM_INICIO])
        self.pinguim.yaw = -math.pi / 2
        self.pinguim.modo = "idle"
        self.pinguim.aplicar()
        self._pos_barco(amb.X_BARCO_INICIO)
        self._helice(1.0)
        self.t_estado = 0.0
        self._ir(Estado.ESPERA)

    # ---------------------------------------------------------------- update
    def atualizar(self, dt):
        self.tempo_total += dt
        self.barco.avancar(dt)
        self.t_estado += dt
        for _ in range(3):                 # se trocou de estado, roda o novo no mesmo quadro
            atual = self.estado
            self._handlers[atual]()
            if self.estado is atual:
                break
        self.pinguim.avancar(dt)

    # ---------------------------------------------------------------- estados
    def _espera(self):
        self._helice(1.0)
        if self.t_estado >= self.c.espera:
            self._ir(Estado.APROXIMACAO, self.c.espera)

    def _aproximacao(self):
        u = limitar(self.t_estado / self.c.aproximacao)
        self._pos_barco(lerp(amb.X_BARCO_INICIO, self.x_parada_a, ease_out(u)))
        self._helice(perfil_helice(u, sobe=0.0, desce=0.4))
        if u >= 1.0:
            self._ir(Estado.PARADA, self.c.aproximacao)

    def _parada(self):
        self._helice(0.0)
        if self.t_estado >= self.c.parada:    # barco parado => libera o pinguim
            self._ir(Estado.CHAMADO, self.c.parada)

    def _chamado(self):
        self.pinguim.modo = "acenar"
        self.pinguim.yaw = lerp_angulo(-math.pi / 2, 0.0, ease_in_out(self.t_estado / 0.8))
        if self.t_estado >= self.c.chamado:
            self._ir(Estado.ATE_A_BORDA, self.c.chamado)

    def _ate_a_borda(self):
        u = limitar(self.t_estado / self.c.ate_a_borda)
        self.pinguim.modo = "andar"
        self.pinguim.pos = np.array([amb.X_DOCA_A, amb.Y_DOCA,
                                     lerp(amb.Z_PINGUIM_INICIO, amb.Z_BORDA, ease_in_out(u))])
        if u >= 1.0:
            self._p0 = self.pinguim.pos.copy()
            self._ir(Estado.SALTO_EMBARQUE, self.c.ate_a_borda)

    def _salto_embarque(self):
        u = limitar(self.t_estado / self.c.salto)
        self.pinguim.modo = "pular"
        alvo = posicao_mundo(self.barco.ponto_embarque)   # alvo MOVEL (barco oscila)
        self.pinguim.pos = parabola(self._p0, alvo, self.c.altura_salto, u)
        if u >= 1.0:
            self.pinguim.anexar_a(self.barco.ponto_embarque)   # vira filho do barco
            self.pinguim.pos = np.zeros(3)                    # encaixa no ponto de embarque
            self.pinguim.aplicar()
            self._ir(Estado.EMBARCADO, self.c.salto)

    def _embarcado(self):
        t = self.t_estado
        self.pinguim.modo = "comemorar" if t < 1.6 else "idle"
        self.pinguim.yaw = lerp_angulo(0.0, math.pi / 2, ease_in_out((t - 1.6) / 0.8))
        self._helice(0.0)
        if t >= self.c.embarcado and self.pinguim_a_bordo():   # condicao de dependencia
            self._ir(Estado.PARTIDA, self.c.embarcado)

    def _partida(self):
        u = limitar(self.t_estado / self.c.partida)
        self._pos_barco(lerp(self.x_parada_a, self.x_parada_b, ease_in_out(u)))
        self._helice(perfil_helice(u, sobe=0.12, desce=0.30))
        self.pinguim.modo = "idle"
        if u >= 1.0:
            self._ir(Estado.CHEGADA, self.c.partida)

    def _chegada(self):
        t = self.t_estado
        self._helice(0.0)
        self.pinguim.modo = "idle"
        self.pinguim.yaw = lerp_angulo(math.pi / 2, math.pi, ease_in_out((t - 0.8) / 0.7))
        if t >= self.c.chegada:
            self.pinguim.anexar_a(self.cena)        # desembarca: volta a ser filho da cena
            self.pinguim.yaw = math.pi
            self._p0 = self.pinguim.pos.copy()
            self._alvo = np.array([amb.X_DOCA_B, amb.Y_DOCA, amb.Z_POUSO_B])
            self._ir(Estado.SALTO_DESEMBARQUE, self.c.chegada)

    def _salto_desembarque(self):
        u = limitar(self.t_estado / self.c.salto)
        self.pinguim.modo = "pular"
        self.pinguim.pos = parabola(self._p0, self._alvo, self.c.altura_salto, u)
        if u >= 1.0:
            self._ir(Estado.DESPEDIDA, self.c.salto)

    def _despedida(self):
        self.pinguim.modo = "acenar"
        self.pinguim.pos = self._alvo.copy()
        self.pinguim.yaw = lerp_angulo(math.pi, 0.0, ease_in_out(self.t_estado / 0.9))
        self._helice(0.0)
        if self.t_estado >= self.c.despedida:     # barco so sai apos a despedida
            self._ir(Estado.SAIDA, self.c.despedida)

    def _saida(self):
        u = limitar(self.t_estado / self.c.saida)
        self._pos_barco(lerp(self.x_parada_b, amb.X_BARCO_FIM, ease_in(u)))
        self._helice(perfil_helice(u, sobe=0.15, desce=0.0))
        self.pinguim.modo = "acenar" if self.t_estado < 2.5 else "idle"
        if u >= 1.0:
            self._ir(Estado.FIM, self.c.saida)

    def _fim(self):
        self.pinguim.modo = "idle"
        if self.t_estado >= self.c.fim:
            self.reiniciar()
