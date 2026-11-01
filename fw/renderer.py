"""Renderer com SHADOW MAPPING (abordagem da secao 6.9 do livro).

Passe 1 (profundidade): a cena e desenhada do ponto de vista da luz em um framebuffer cuja
unica saida e uma textura de profundidade (o shadow map).
Passe 2 (cor): a cena e desenhada da camera; cada fragmento e transformado para o espaco da
luz e comparado com o shadow map -> se estiver mais longe que o valor gravado, esta em sombra.
"""
import numpy as np
from OpenGL.GL import *  # noqa: F401,F403
import pygame

from fw import shaders
from fw.camera import olhar_para, ortografica
from fw.light import AmbientLight, DirectionalLight
from fw.material import Material


class Programa:
    def __init__(self, vs, fs):
        self.id = glCreateProgram()
        for tipo, codigo in ((GL_VERTEX_SHADER, vs), (GL_FRAGMENT_SHADER, fs)):
            sh = glCreateShader(tipo)
            glShaderSource(sh, codigo)
            glCompileShader(sh)
            if not glGetShaderiv(sh, GL_COMPILE_STATUS):
                raise RuntimeError(glGetShaderInfoLog(sh).decode())
            glAttachShader(self.id, sh)
        glLinkProgram(self.id)
        if not glGetProgramiv(self.id, GL_LINK_STATUS):
            raise RuntimeError(glGetProgramInfoLog(self.id).decode())
        self._loc = {}

    def usar(self):
        glUseProgram(self.id)

    def set(self, nome, v):
        if nome not in self._loc:
            self._loc[nome] = glGetUniformLocation(self.id, nome)
        loc = self._loc[nome]
        if loc < 0:
            return
        if isinstance(v, (bool, int)):
            glUniform1i(loc, int(v))
        elif isinstance(v, float):
            glUniform1f(loc, v)
        else:
            a = np.asarray(v, np.float32)
            if a.shape == (4, 4):
                glUniformMatrix4fv(loc, 1, GL_TRUE, a)
            elif a.shape == (3, 3):
                glUniformMatrix3fv(loc, 1, GL_TRUE, a)
            elif a.shape == (3,):
                glUniform3f(loc, *a)
            elif a.shape == (2,):
                glUniform2f(loc, *a)


class Renderer:
    def __init__(self, clear_color=(0.5, 0.7, 0.9)):
        self.clear_color = clear_color
        glEnable(GL_DEPTH_TEST)
        self.prog = Programa(shaders.VERTEX_PRINCIPAL, shaders.FRAGMENT_PRINCIPAL)
        self.prog_prof = Programa(shaders.VERTEX_PROFUNDIDADE, shaders.FRAGMENT_PROFUNDIDADE)
        self.luz_sombra = None
        self.material_padrao = Material()

    def enable_shadows(self, luz, strength=0.8, resolution=(2048, 2048),
                       bounds=(-30, 30, -20, 20, 1, 70), bias=0.004):
        """Cria o framebuffer do shadow map (textura de profundidade) para a luz direcional."""
        self.luz_sombra = luz
        self.sombra_forca = strength
        self.sombra_bias = bias
        self.sombra_res = tuple(resolution)
        self.sombra_bounds = bounds
        self.tex_sombra = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.tex_sombra)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT24, resolution[0], resolution[1], 0,
                     GL_DEPTH_COMPONENT, GL_FLOAT, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
        glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, [1.0, 1.0, 1.0, 1.0])  # fora = iluminado
        self.fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, self.tex_sombra, 0)
        glDrawBuffer(GL_NONE)
        glReadBuffer(GL_NONE)
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            raise RuntimeError("framebuffer do shadow map incompleto")
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def _matriz_luz(self):
        luz = self.luz_sombra
        olho = luz.get_world_position()
        visao = olhar_para(olho, olho + luz.direction)
        return ortografica(*self.sombra_bounds) @ visao

    @staticmethod
    def _matriz_normal(m):
        return np.linalg.inv(m[:3, :3]).T

    def render(self, cena, camera):
        nos = cena.descendants()
        malhas = [n for n in nos if hasattr(n, "geometry") and getattr(n, "visible", True)]
        ambiente = np.zeros(3)
        sol = None
        for n in nos:
            if isinstance(n, AmbientLight):
                ambiente = ambiente + n.color
            elif isinstance(n, DirectionalLight) and sol is None:
                sol = n
        mundos = {id(m): m.get_world_matrix() for m in malhas}

        # ---------------- passe 1: shadow map ----------------
        if self.luz_sombra is not None:
            luz_m = self._matriz_luz()
            glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
            glViewport(0, 0, *self.sombra_res)
            glClear(GL_DEPTH_BUFFER_BIT)
            glEnable(GL_POLYGON_OFFSET_FILL)
            glPolygonOffset(2.0, 4.0)
            self.prog_prof.usar()
            self.prog_prof.set("lightMatrix", luz_m)
            for m in malhas:
                if m.cast_shadow:
                    self.prog_prof.set("modelMatrix", mundos[id(m)])
                    m.geometry.desenhar()
            glDisable(GL_POLYGON_OFFSET_FILL)
            glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # ---------------- passe 2: cor ----------------
        w, h = pygame.display.get_surface().get_size()
        glViewport(0, 0, w, h)
        glClearColor(*self.clear_color, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        p = self.prog
        p.usar()
        p.set("viewMatrix", camera.view_matrix())
        p.set("projectionMatrix", camera.projection)
        p.set("viewPos", camera.get_world_position())
        p.set("ambientColor", ambiente)
        if sol is not None:
            p.set("lightColor", sol.color)
            p.set("lightDir", sol.direction)
        else:
            p.set("lightColor", np.zeros(3))
            p.set("lightDir", np.array([0, -1, 0.0]))
        sombra_on = self.luz_sombra is not None
        p.set("shadowOn", sombra_on)
        if sombra_on:
            p.set("lightMatrix", luz_m)
            p.set("shadowStrength", float(self.sombra_forca))
            p.set("shadowBias", float(self.sombra_bias))
            glActiveTexture(GL_TEXTURE1)
            glBindTexture(GL_TEXTURE_2D, self.tex_sombra)
            p.set("shadowMap", 1)
        for m in malhas:
            mat = m.material
            mundo = mundos[id(m)]
            p.set("modelMatrix", mundo)
            p.set("normalMatrix", self._matriz_normal(mundo))
            p.set("baseColor", mat.cor)
            p.set("shininess", mat.brilho)
            p.set("specularStrength", mat.especular)
            p.set("repeatUV", mat.repeticao)
            glActiveTexture(GL_TEXTURE0)
            if mat.textura is not None:
                glBindTexture(GL_TEXTURE_2D, mat.textura.id)
                p.set("useTexture", True)
            else:
                p.set("useTexture", False)
            p.set("tex", 0)
            m.geometry.desenhar()
