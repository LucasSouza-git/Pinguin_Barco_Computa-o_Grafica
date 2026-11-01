"""Renderiza quadros deterministicos da cena e salva PNG (para conferir/ilustrar o relatorio).
Uso:  python tools/captura.py   (em Linux sem monitor: xvfb-run -a python tools/captura.py)
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cena.app import AplicacaoCena

SAIDA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "capturas")
INSTANTES = [1.0, 8.5, 14.0, 15.0, 21.0, 36.0]   # s: espera, chegada, chamado, salto, viagem, despedida
DT = 1 / 60


def apos(app, n):
    t = n * DT
    for alvo in INSTANTES:
        if abs(t - alvo) < DT / 2:
            os.makedirs(SAIDA, exist_ok=True)
            app.capturar(os.path.join(SAIDA, f"t{alvo:05.1f}_{app.diretor.estado.name}.png"))


if __name__ == "__main__":
    AplicacaoCena().run(dt_fixo=DT, max_quadros=int(max(INSTANTES) / DT) + 2, apos_quadro=apos)
