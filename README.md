# Pinguim e Barco a Motor — Computação Gráfica (UNIPAC, 2026/02)

## 1. Identificação
| Integrante | Tema sorteado |
|---|---|
| _(nome 1)_ | Pinguim de brinquedo |
| _(nome 2)_ | Barco a motor |

## 2. Cena e interação
Lago de demonstração com margem nevada e duas docas (A e B). O barco chega à doca A e **para**;
só então o pinguim recebe o "sinal": vira, acena, anda até a borda e **salta** para o convés.
Ao pousar, o pinguim **vira filho do barco no grafo de cena** (acompanha a oscilação sem cálculo extra).
O barco **só parte** depois do embarque, navega até a doca B e para; o pinguim desembarca, se despede,
e **somente depois da despedida** o barco deixa a doca. Depois de alguns segundos o ciclo reinicia.
As ações são encadeadas por etapas (sem simulação física), conforme o enunciado.

## 3. Instalação e execução
**Versão do Python: 3.12** (o projeto foi desenvolvido e testado nela; o Pygame pode não funcionar em versões mais novas, como a 3.14).

Windows (PowerShell/CMD):
```
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python tools/gerar_texturas.py      # só se a pasta imagens/ estiver vazia
python main.py
```
Linux/macOS:
```
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```
Verifique a versão ativa com `python --version` (deve mostrar 3.12.x).

Requisitos: Python 3.12, `pygame` 2.6.x, `PyOpenGL` 3.1.x e `numpy` (OpenGL 3.3 core ou superior).
Sem monitor (Linux): `xvfb-run -a python tools/captura.py` gera quadros PNG em `capturas/`.

### Sobre o framework (`fw/`)
O enunciado pede o framework do livro. Esta versão usa o pacote `fw/`, um **mini-framework próprio
que segue a arquitetura do livro** (Object3D/grafo de cena, Geometry, Material, Light, Camera,
MovementRig, Renderer com shadow mapping da seção 6.9, Base com laço e delta time), escrito para
rodar de forma autônoma e testável. Todo o código da cena (`cena/`) só acessa o framework por
`cena/fabrica.py`; para usar o framework do livro, basta reimplementar esse arquivo.
**Confirmem com o professor se `fw/` é aceito ou se é preciso migrar para o código original do livro,
e identifiquem a fonte (livro) nas partes adaptadas.**

## 4. Controles
| Tecla | Ação |
|---|---|
| W / A / S / D | mover a câmera |
| R / F | subir / descer |
| Q / E | girar (esquerda / direita) |
| T / G | olhar para cima / baixo |
| **P** | pausar / retomar a animação (a câmera continua livre e o render não para) |
| **X** | reiniciar a sequência |

## 5. Onde está cada recurso gráfico
| Requisito | Onde |
|---|---|
| Modelos por composição de formas | `cena/pinguim.py` (`Pinguim.__init__`), `cena/barco.py` (`Barco.__init__`), `cena/ambiente.py` |
| Delta time (independente de FPS) | `cena/app.py` (`update`, `DT_MAX`), `cena/interacao.py` (`Diretor.atualizar`, `t_estado`) |
| Translação, rotação, escala | `cena/transformacoes.py` (`compor`); escala: squash/stretch em `Pinguim.avancar`, bico/pés/corpo em `criar_esfera` |
| Hierarquia (grafo de cena) | árvores descritas nos docstrings de `pinguim.py` e `barco.py`; reparentar: `Pinguim.anexar_a` |
| Máquina de estados / interação | `cena/interacao.py` (`Diretor`, `Estado`, `Tempos`) |
| Câmera em perspectiva + teclado | `cena/app.py` (`Camera`, `MovementRig`) |
| Pausa sem parar o render | `cena/app.py` (`update`: `dt = 0` quando pausado) |
| Texturas + UV | `fw/material.py` (`Texture`), `fw/geometry.py` (UV por face), uniform `repeatUV`; usadas em `ambiente.py` e `barco.py` |
| Iluminação direcional + normais | `fw/light.py`, `fw/shaders.py` (Phong), `fw/geometry.py` (normais por face/esfera; `escalar` corrige normais), `normalMatrix` em `fw/renderer.py` |
| Sombra (shadow mapping, seção 6.9) | `fw/renderer.py` (`enable_shadows`, passe de profundidade + passe de cor), `fw/shaders.py` (`calcSombra`, PCF 3x3) |
| Shaders | `fw/shaders.py` (GLSL) |

## 6. Contribuições individuais
_(preencher: quem fez pinguim, barco, ambiente, interação, README…)_

## 7. Fontes consultadas
- STEMKOSKI, L.; PASCALE, M. *Developing Graphics Frameworks with Python and OpenGL*. CRC Press, 2022 (framework e seção 6.9).
- Texturas: geradas por `tools/gerar_texturas.py` (ver `imagens/LICENCAS.txt`).

## 8. Uso de inteligência artificial (declaração)
- **Ferramenta:** Claude (Anthropic).
- **Finalidade:** planejamento da interação, estrutura de arquivos/classes e geração inicial do código da pasta `cena/`, dos testes e do gerador de texturas.
- **Trechos:** `cena/*.py`, `tools/gerar_texturas.py`, `tests/test_interacao_sem_gl.py`. _(Liste o que foi revisado/alterado por vocês.)_

## 9. Shaders, atributos e uniforms (resumo para a apresentação)
- **Atributos de vértice** (VBO intercalado): `vertexPosition` (loc 0), `vertexNormal` (loc 1), `vertexUV` (loc 2).
- **Vertex shader principal:** `modelMatrix` leva o vértice ao mundo (hierarquia incluída), `viewMatrix` e
  `projectionMatrix` à tela; `normalMatrix` (= transposta da inversa de `mat3(modelMatrix)`) corrige as normais;
  `lightMatrix` leva o ponto ao espaço da luz; `repeatUV` repete a textura.
- **Fragment shader:** modelo de Phong (`ambientColor`, difusa com `lightDir`/`lightColor`, especular com
  `viewPos`, `shininess`, `specularStrength`), cor `baseColor` × textura (`useTexture`, `tex`).
- **Sombreamento x sombra:** *sombreamento* é o escurecimento de uma superfície pelo ângulo entre normal e luz
  (`difusa`); *sombra projetada* é um objeto bloqueando a luz de outro (`calcSombra`, que compara a profundidade
  do fragmento no espaço da luz com o `shadowMap`, usando `shadowBias` contra "acne" e PCF para suavizar).
- **Passe de sombra:** só `modelMatrix` e `lightMatrix`; fragment shader vazio (grava apenas a profundidade).

## 10. Teste da lógica sem OpenGL
```
python -m tests.test_interacao_sem_gl
```
Verifica a ordem dos estados, as dependências entre os personagens, a continuidade do movimento,
a independência da taxa de quadros (30/60/144 FPS) e o congelamento na pausa.
