"""Aplicacao principal: janela, camera, luzes, sombra, pausa e laco de render.

Estrutura Base.initialize()/update() inspirada no livro (STEMKOSKI; PASCALE, 2022).
"""
import numpy as np

from fw.base import Base
from fw.camera import Camera, MovementRig
from fw.light import AmbientLight, DirectionalLight
from fw.object3d import Object3D
from fw.renderer import Renderer

from cena.ambiente import Ambiente
from cena.barco import Barco
from cena.pinguim import Pinguim
from cena.interacao import Diretor

DT_MAX = 0.05   # limita saltos de tempo (ex.: ao arrastar a janela)


class AplicacaoCena(Base):
    def initialize(self):
        print("Controles: W/A/S/D mover | R/F subir/descer | Q/E girar | T/G olhar cima/baixo"
              " | P pausar/retomar | X reiniciar | ESC sair")
        self.renderer = Renderer(clear_color=(0.62, 0.78, 0.95))
        self.scene = Object3D()

        # camera em perspectiva dentro de um "rig" controlado pelo teclado
        w, h = self.screen_size
        self.camera = Camera(angle_of_view=60, aspect_ratio=w / h)
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.pitch = -0.29
        self.rig.set_position([1.5, 4.2, 9.5])
        self.scene.add(self.rig)

        # luz ambiente + luz direcional (o "sol") que gera o shadow map
        self.scene.add(AmbientLight(color=[0.38, 0.40, 0.48]))
        self.sol = DirectionalLight(color=[0.95, 0.92, 0.82], direction=[-0.8, -1.0, -0.45])
        self.sol.set_position(np.array([18.0, 22.0, 5.0]))   # a camera de sombra nasce aqui
        self.scene.add(self.sol)
        self.renderer.enable_shadows(self.sol, strength=0.85, resolution=(2048, 2048),
                                     bounds=(-30, 30, -20, 20, 1, 70))

        # personagens e ambiente
        self.scene.add(Ambiente())
        self.barco = Barco()
        self.scene.add(self.barco)
        self.pinguim = Pinguim()                # o Diretor o adiciona a cena em reiniciar()
        self.diretor = Diretor(self.scene, self.barco, self.pinguim)
        self.pausado = False

    def update(self):
        if self.input.is_key_pressed("p"):
            self.pausado = not self.pausado
        if self.input.is_key_pressed("x"):
            self.diretor.reiniciar()

        # a camera usa o tempo REAL (continua se movendo com a animacao pausada)
        self.rig.update(self.input, self.delta_time)

        # a animacao usa dt = 0 quando pausada; o render nunca para
        dt = 0.0 if self.pausado else min(self.delta_time, DT_MAX)
        self.diretor.atualizar(dt)

        self.renderer.render(self.scene, self.camera)
