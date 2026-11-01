"""Ambiente: lago, margem nevada e duas docas (A: embarque, B: desembarque).

O barco navega ao longo de +X na linha z = Z_BARCO; as docas ficam na margem norte (-Z).
Expoe as constantes que o Diretor usa para sincronizar os dois personagens.
"""
from cena.fabrica import (Object3D, criar_caixa, criar_cilindro, criar_plano_horizontal,
                          posicionar, carregar_textura)

# --- geometria do cenario (unidades arbitrarias; pinguim ~1.4 de altura) ------
X_DOCA_A = -4.0
X_DOCA_B = 9.0
Z_BARCO = -4.0           # linha do trajeto do barco
Y_DOCA = 0.40            # altura do tampo das docas (= altura do deck do barco)
Z_PINGUIM_INICIO = -8.0  # onde o pinguim espera na doca
Z_BORDA = -5.95          # onde ele para para saltar (borda da doca = -5.5)
Z_POUSO_B = -6.6         # onde ele pousa na doca B
X_BARCO_INICIO = -22.0
X_BARCO_FIM = 26.0


class Ambiente(Object3D):
    def __init__(self):
        super().__init__()
        madeira = carregar_textura("madeira.png")

        # lago (textura de agua, UV repetido 12x)
        agua = criar_plano_horizontal(80, 80, textura=carregar_textura("agua.png"),
                                      repeticao=(12, 12), cor=(0.8, 0.9, 1.0),
                                      brilho=96, especular=0.8)
        self.add(agua)

        # margem nevada ao norte
        margem = criar_caixa(80, 0.6, 24, textura=carregar_textura("neve.png"),
                             repeticao=(10, 3), brilho=8, especular=0.1)
        posicionar(margem, (0, 0.1, -21.5))
        self.add(margem)

        # docas: tampo de madeira + estacas na borda
        for x in (X_DOCA_A, X_DOCA_B):
            doca = criar_caixa(5.0, 0.6, 4.0, textura=madeira, repeticao=(2, 1),
                               brilho=8, especular=0.1)
            posicionar(doca, (x, 0.1, -7.5))
            self.add(doca)
            for dx in (-2.3, 2.3):
                estaca = criar_cilindro(0.09, 1.1, (0.35, 0.22, 0.12))
                posicionar(estaca, (x + dx, 0.45, -5.65))
                self.add(estaca)

        # blocos de gelo decorativos (tambem recebem/projetam sombra)
        for (x, z, l, a, p, giro) in [(-14, -12, 3.0, 2.0, 2.5, 0.5),
                                      (3, -13, 2.2, 1.4, 2.0, -0.4),
                                      (17, -11, 3.5, 2.6, 3.0, 0.9)]:
            bloco = criar_caixa(l, a, p, (0.75, 0.9, 1.0), brilho=128, especular=0.9)
            posicionar(bloco, (x, 0.4 + a / 2 - 0.1, z), ry=giro)
            self.add(bloco)
