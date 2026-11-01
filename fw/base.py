"""Base: janela Pygame + contexto OpenGL 3.3 core, entrada e laco principal com delta time."""
import pygame
import numpy as np
from OpenGL.GL import glReadPixels, GL_RGB, GL_UNSIGNED_BYTE


class Input:
    def __init__(self):
        self.down, self.pressed, self.quit = set(), set(), False

    def update(self, eventos):
        self.pressed.clear()
        for e in eventos:
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                self.quit = True
            elif e.type == pygame.KEYDOWN:
                nome = pygame.key.name(e.key)
                self.down.add(nome)
                self.pressed.add(nome)
            elif e.type == pygame.KEYUP:
                self.down.discard(pygame.key.name(e.key))

    def is_key_down(self, k):
        return k in self.down

    def is_key_pressed(self, k):
        return k in self.pressed


class Base:
    def __init__(self, screen_size=(960, 640), titulo="Pinguim e Barco - Computacao Grafica"):
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.set_mode(tuple(screen_size), pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption(titulo)
        self.screen_size = tuple(screen_size)
        self.input = Input()
        self.delta_time = 0.0
        self.time = 0.0

    def initialize(self):
        pass

    def update(self):
        pass

    def capturar(self, caminho):
        """Salva o quadro atual em PNG (usado nos testes/relatorio)."""
        w, h = self.screen_size
        dados = glReadPixels(0, 0, w, h, GL_RGB, GL_UNSIGNED_BYTE)
        img = np.frombuffer(dados, np.uint8).reshape(h, w, 3)[::-1]
        pygame.image.save(pygame.image.frombuffer(img.tobytes(), (w, h), "RGB"), caminho)

    def run(self, dt_fixo=None, max_quadros=None, apos_quadro=None):
        """dt_fixo/max_quadros/apos_quadro: modo deterministico para testes sem janela interativa."""
        self.initialize()
        relogio = pygame.time.Clock()
        n = 0
        while not self.input.quit:
            self.delta_time = dt_fixo if dt_fixo else relogio.tick(120) / 1000.0
            self.time += self.delta_time
            self.input.update(pygame.event.get())
            self.update()
            pygame.display.flip()
            n += 1
            if apos_quadro:
                apos_quadro(self, n)
            if max_quadros and n >= max_quadros:
                break
        pygame.quit()
