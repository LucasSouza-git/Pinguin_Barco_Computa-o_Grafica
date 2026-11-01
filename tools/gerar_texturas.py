"""Gera as texturas (PNG 512x512, sem emenda) usadas na cena.

Origem das imagens: 100% procedurais, geradas por este script (autoria da dupla),
portanto sem direitos de terceiros.   Uso:  python tools/gerar_texturas.py
"""
import os
import numpy as np
from PIL import Image

N = 512
rng = np.random.default_rng(7)
DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "imagens")


def ruido(sx, sy=None):
    """Ruido periodico (FFT) com suavizacao sx/sy -> as bordas casam (tile perfeito)."""
    sy = sx if sy is None else sy
    f = np.fft.fft2(rng.standard_normal((N, N)))
    ky = np.fft.fftfreq(N)[:, None]
    kx = np.fft.fftfreq(N)[None, :]
    filtro = np.exp(-((kx * sx) ** 2 + (ky * sy) ** 2) * (2 * np.pi) ** 2 / 2)
    r = np.real(np.fft.ifft2(f * filtro))
    r -= r.min()
    return r / r.max()


def salvar(nome, rgb):
    img = (np.clip(rgb, 0, 1) * 255).astype(np.uint8)
    Image.fromarray(img, "RGB").save(os.path.join(DEST, nome))
    print("gerada:", nome)


def agua():
    y, x = np.mgrid[0:N, 0:N] / N
    ondas = 0.5 + 0.5 * np.sin(2 * np.pi * (6 * y + 3 * x) + 4 * ruido(8))
    base = 0.55 * ruido(14) + 0.45 * ondas
    cor = np.array([0.08, 0.32, 0.55]) + base[..., None] * np.array([0.10, 0.18, 0.18])
    salvar("agua.png", cor)


def madeira():
    img = np.zeros((N, N, 3))
    n_tabuas = 8
    alt = N // n_tabuas
    veio = ruido(30.0, 1.2)                    # fibras alongadas na horizontal
    for i in range(n_tabuas):
        tom = 0.75 + 0.25 * rng.random()
        base = np.array([0.55, 0.36, 0.20]) * tom
        bloco = base + (veio[i * alt:(i + 1) * alt, :, None] - 0.5) * 0.25
        img[i * alt:(i + 1) * alt] = bloco
        img[i * alt:i * alt + 3] *= 0.45       # fresta entre tabuas
    salvar("madeira.png", img)


def neve():
    base = 0.90 + 0.06 * ruido(10) + 0.04 * ruido(1.5)
    cor = np.stack([base * 0.96, base * 0.98, base * 1.0], axis=-1)
    salvar("neve.png", cor)


if __name__ == "__main__":
    os.makedirs(DEST, exist_ok=True)
    agua()
    madeira()
    neve()
