"""Valida a maquina de estados SEM OpenGL: substitui cena.fabrica por um framework falso.

Executar na raiz do projeto:  python -m tests.test_interacao_sem_gl
"""
import sys
import types

import numpy as np


# ------------------------- framework falso (so grafo de cena) ------------------
class Object3D:
    def __init__(self):
        self.transform = np.eye(4)
        self.parent = None
        self.children_list = []

    def add(self, c):
        c.parent = self
        self.children_list.append(c)

    def remove(self, c):
        self.children_list.remove(c)
        c.parent = None


def _malha(*a, **k):
    return Object3D()


fake = types.ModuleType("cena.fabrica")
fake.Object3D = Object3D
fake.criar_caixa = _malha
fake.criar_esfera = _malha
fake.criar_cilindro = _malha
fake.criar_plano_horizontal = _malha
fake.carregar_textura = lambda nome: None


def _posicionar(obj, pos=(0, 0, 0), rx=0.0, ry=0.0, rz=0.0, escala=(1, 1, 1)):
    from cena.transformacoes import compor
    obj.transform = compor(pos, rx, ry, rz, escala)
    return obj


fake.posicionar = _posicionar
sys.modules["cena.fabrica"] = fake

from cena.ambiente import Ambiente                      # noqa: E402
from cena.barco import Barco                            # noqa: E402
from cena.pinguim import Pinguim                        # noqa: E402
from cena.interacao import Diretor, Estado             # noqa: E402
from cena.transformacoes import posicao_mundo          # noqa: E402


def montar():
    cena = Object3D()
    cena.add(Ambiente())
    barco = Barco()
    cena.add(barco)
    pinguim = Pinguim()
    d = Diretor(cena, barco, pinguim)
    return cena, barco, pinguim, d


def simular(fps, segundos_max=80):
    cena, barco, pinguim, d = montar()
    dt = 1.0 / fps
    ordem = [d.estado]
    max_salto_mundo = 0.0
    anterior = posicao_mundo(pinguim)
    violacoes = []
    t = 0.0
    while t < segundos_max:
        x_antes = barco.x
        estado_antes = d.estado
        d.atualizar(dt)
        t += dt
        if d.estado != ordem[-1]:
            ordem.append(d.estado)
        # regra: barco so se move em APROXIMACAO, PARTIDA e SAIDA
        if abs(barco.x - x_antes) > 1e-9 and d.estado not in (
                Estado.APROXIMACAO, Estado.PARTIDA, Estado.SAIDA, Estado.FIM) \
                and estado_antes not in (Estado.APROXIMACAO, Estado.PARTIDA, Estado.SAIDA, Estado.FIM):
            violacoes.append(("barco moveu fora de hora", estado_antes))
        # regra: PARTIDA exige pinguim a bordo
        if Estado.PARTIDA in (estado_antes, d.estado) and not d.pinguim_a_bordo():
            violacoes.append(("partida sem pinguim a bordo", t))
        # regra: pinguim so age depois que o barco parou
        if estado_antes in (Estado.CHAMADO, Estado.ATE_A_BORDA, Estado.SALTO_EMBARQUE) \
                and abs(barco.x - d.x_parada_a) > 1e-6:
            violacoes.append(("pinguim agiu com barco em movimento", t))
        atual = posicao_mundo(pinguim)
        if d.estado != Estado.ESPERA or ordem[-1] != Estado.ESPERA:
            max_salto_mundo = max(max_salto_mundo, np.linalg.norm(atual - anterior) * (fps / 60.0))
        anterior = atual
        if len(ordem) > 13 and d.estado == Estado.ESPERA:
            break  # completou um ciclo e reiniciou
    return t, ordem, max_salto_mundo, violacoes


ESPERADO = [Estado.ESPERA, Estado.APROXIMACAO, Estado.PARADA, Estado.CHAMADO, Estado.ATE_A_BORDA,
            Estado.SALTO_EMBARQUE, Estado.EMBARCADO, Estado.PARTIDA, Estado.CHEGADA,
            Estado.SALTO_DESEMBARQUE, Estado.DESPEDIDA, Estado.SAIDA, Estado.FIM, Estado.ESPERA]


def main():
    duracoes = []
    for fps in (30, 60, 144):
        t, ordem, salto, viol = simular(fps)
        assert ordem == ESPERADO, f"ordem errada a {fps} fps: {ordem}"
        assert not viol, f"violacoes a {fps} fps: {viol[:3]}"
        assert salto < 0.25, f"pulo visual (descontinuidade) de {salto:.3f} a {fps} fps"
        duracoes.append(t)
        print(f"{fps:>4} fps: ciclo completo em {t:6.2f} s | maior passo do pinguim/quadro(60fps) = {salto:.3f}")
    assert max(duracoes) - min(duracoes) < 0.1, "duracao depende da taxa de quadros!"

    # pausa: dt = 0 nao altera nada
    cena, barco, pinguim, d = montar()
    for _ in range(300):
        d.atualizar(1 / 60)
    snap = (d.estado, d.t_estado, barco.x, pinguim.t_anim)
    for _ in range(300):
        d.atualizar(0.0)
    assert snap == (d.estado, d.t_estado, barco.x, pinguim.t_anim), "pausa nao congelou a animacao"
    print("OK: ordem dos estados, dependencias, continuidade, independencia de FPS e pausa.")


if __name__ == "__main__":
    main()
