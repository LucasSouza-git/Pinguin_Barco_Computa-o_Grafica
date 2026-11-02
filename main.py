import sys

if sys.version_info[:2] != (3, 12):
    print(f"AVISO: este projeto foi desenvolvido e testado com Python 3.12 "
          f"(versao atual: {sys.version_info.major}.{sys.version_info.minor}). "
          f"Se o Pygame nao instalar ou nao abrir a janela, use o Python 3.12.")

from cena.app import AplicacaoCena  # noqa: E402

if __name__ == "__main__":
    AplicacaoCena(screen_size=(960, 640)).run()
