# Pinguim e Barco a Motor — Computação Gráfica

Trabalho prático desenvolvido para a disciplina de Computação Gráfica do curso de Ciência da Computação da UNIPAC Barbacena, período 2026/02.

## 1. Identificação

| Integrante | Tema sorteado |
|---|---|
| Lucas de Souza Carmo 242-009065 | Pinguim de brinquedo |
| Carlos Eduardo Santos Almeida 231-001461 | Barco a motor |

## 2. Descrição da cena e interação

O projeto consiste em uma aplicação gráfica tridimensional que representa um pinguim de brinquedo e um barco a motor em um lago de demonstração, com margem nevada e duas docas.

A cena apresenta uma sequência de ações coordenadas entre os dois personagens:

1. O barco se desloca até a doca A e interrompe seu movimento.
2. O pinguim recebe o sinal para iniciar sua movimentação, vira-se, acena e caminha até a borda.
3. O pinguim salta para o convés do barco e passa a acompanhar seus movimentos.
4. O barco inicia seu percurso até a doca B, transportando o pinguim.
5. Ao chegar à segunda doca, o pinguim desembarca e realiza uma despedida.
6. Após o término da interação, o barco deixa a doca e a sequência é reiniciada.

A interação foi implementada por meio de etapas sequenciais, utilizando uma máquina de estados para controlar os movimentos e as ações dos personagens, sem necessidade de simulação física.

## 3. Tecnologias, framework e instalação

### 3.1 Tecnologias utilizadas

- **Python 3.12:** linguagem utilizada no desenvolvimento da aplicação.
- **Pygame 2.6.x:** biblioteca utilizada para gerenciamento da janela, entrada do teclado e execução da aplicação.
- **PyOpenGL 3.1.x:** biblioteca utilizada para acessar os recursos gráficos da OpenGL.
- **NumPy:** utilizada em operações matemáticas e manipulação de vetores e matrizes.
- **OpenGL 3.3 Core:** interface gráfica utilizada para renderização tridimensional.
- **GLSL:** linguagem utilizada na implementação dos shaders.

### 3.2 Framework gráfico

O desenvolvimento segue a arquitetura apresentada no livro *Developing Graphics Frameworks with Python and OpenGL* (STEMKOSKI; PASCALE, 2022). A pasta `fw/` contém uma **versão compacta do framework, reescrita pela dupla** a partir das ideias do livro (nomes e organização adaptados), contendo apenas os componentes efetivamente usados na cena. Não há cópia integral do código do livro.

| Arquivo | Componente | Relação com o livro |
|---|---|---|
| `fw/base.py` | `Base`, `Input`: janela Pygame, contexto OpenGL 3.3 core, entrada e laço principal com *delta time* | Estrutura `initialize()` / `update()` do livro |
| `fw/object3d.py` | `Object3D`: nó do grafo de cena (`add`, `remove`, `get_world_matrix`, `descendants`) | Grafo de cena (capítulo 4) |
| `fw/matrix.py` | Matrizes 4x4 de translação, rotação e escala (`compor`) | Transformações geométricas |
| `fw/camera.py` | `Camera` (perspectiva), `MovementRig` (controle por teclado), `olhar_para`, `ortografica` | Câmera e *rig* de movimento |
| `fw/geometry.py` | `caixa`, `esfera`, `cilindro`, `retangulo` (posição, normal e UV por vértice) | Geometrias |
| `fw/material.py` | `Texture`, `Material` (cor, textura, brilho, especular, repetição de UV) | Texturas e materiais |
| `fw/light.py` | `AmbientLight`, `DirectionalLight` | Luzes |
| `fw/mesh.py` | `Mesh`: geometria + material + `cast_shadow` | Malha |
| `fw/shaders.py` | Código GLSL dos shaders (principal e de profundidade) | Shaders |
| `fw/renderer.py` | `Renderer`: dois passes, com *shadow mapping* | Seção 6.9 (sombras) |

A camada `cena/fabrica.py` funciona como adaptador entre o código da cena (pinguim, barco, ambiente) e o framework em `fw/`.

Conceitos utilizados: grafo de cena, geometria por composição de formas, translação/rotação/escala, materiais e texturas, câmera em perspectiva, iluminação direcional (modelo de Phong), shaders e *shadow mapping*.

### 3.3 Instalação e execução

**Versão recomendada:** Python 3.12.

#### Windows

```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python tools/gerar_texturas.py
python main.py
```

O comando de geração de texturas deve ser executado somente quando necessário, caso a pasta `imagens/` esteja vazia.

#### Linux/macOS

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Para verificar a versão instalada:

```bash
python --version
```

## 4. Controles

| Tecla | Ação |
|---|---|
| W / A / S / D | Movimentar a câmera |
| R / F | Subir / descer |
| Q / E | Girar para esquerda / direita |
| T / G | Olhar para cima / baixo |
| P | Pausar / retomar a animação |
| X | Reiniciar a sequência |

A pausa interrompe a animação dos personagens, mantendo a visualização e o controle da câmera ativos.

## 5. Recursos gráficos implementados

| Recurso | Implementação |
|---|---|
| Modelagem tridimensional | Composição de formas geométricas para representar o pinguim, o barco e o ambiente |
| Animação | Movimentos controlados pelo tempo decorrido, independentemente da taxa de quadros |
| Transformações geométricas | Translação, rotação e escala |
| Hierarquia de objetos | Organização dos componentes dos personagens por meio do grafo de cena |
| Interação | Máquina de estados responsável pela coordenação dos movimentos |
| Câmera | Projeção em perspectiva e controle pelo teclado |
| Texturas | Aplicação de imagens às superfícies com coordenadas UV |
| Iluminação | Iluminação direcional e materiais com modelo de reflexão de Phong |
| Sombras | Shadow mapping, conforme a abordagem apresentada na seção 6.9 do livro |
| Shaders | Vertex shaders e fragment shaders desenvolvidos em GLSL |

### Principais arquivos do projeto

| Arquivo / diretório | Responsabilidade | Classes / funções principais |
|---|---|---|
| `main.py` | Inicialização da aplicação | |
| `cena/app.py` | Controle da aplicação: câmera, luzes, pausa e laço de render | `AplicacaoCena` |
| `cena/interacao.py` | Máquina de estados que coordena pinguim e barco | `Diretor`, `Estado`, `Tempos` |
| `cena/pinguim.py` | Modelagem hierárquica e animação procedural do pinguim | `Pinguim.avancar`, `Pinguim.anexar_a` |
| `cena/barco.py` | Modelagem do barco, oscilação e hélice | `Barco.aplicar`, `Barco.avancar` |
| `cena/ambiente.py` | Lago, margem nevada, docas e blocos de gelo | `Ambiente` |
| `cena/fabrica.py` | Adaptador entre a cena e o framework | `criar_caixa`, `criar_esfera`, `carregar_textura`, `posicionar` |
| `cena/transformacoes.py` | Matriz e posição no mundo, extração de posição e giro | `matriz_mundo`, `posicao_mundo` |
| `cena/utils_anim.py` | Funções de interpolação e suavização | `lerp`, `ease_in_out`, `parabola`, `lerp_angulo` |
| `fw/` | Framework gráfico (ver seção 3.2) | |
| `fw/shaders.py` | Shaders GLSL | `VERTEX_PRINCIPAL`, `FRAGMENT_PRINCIPAL`, `VERTEX_PROFUNDIDADE` |
| `fw/renderer.py` | Renderização e shadow mapping | `Renderer.enable_shadows`, `Renderer.render` |
| `imagens/` | Texturas (`agua.png`, `madeira.png`, `neve.png`) e `LICENCAS.txt` | |
| `capturas/` | Capturas de tela de etapas da animação | |
| `tools/gerar_texturas.py` | Geração das texturas | |
| `tools/captura.py` | Renderização determinística de quadros para as capturas | |
| `tests/test_interacao_sem_gl.py` | Testes da lógica de interação, sem OpenGL | |

## 6. Contribuições individuais

### Lucas — Modelagem e animação do pinguim

Responsável pelo desenvolvimento do modelo tridimensional do pinguim, incluindo:

- Construção do personagem por composição de formas geométricas.
- Organização hierárquica das partes do modelo.
- Implementação dos movimentos de caminhada, aceno e salto.
- Integração do personagem à sequência de interação.
- Ajustes e testes relacionados à movimentação do pinguim.

### Carlos — Modelagem do barco e integração da cena

Responsável pelo desenvolvimento do barco e pela integração dos elementos da cena, incluindo:

- Construção do modelo tridimensional do barco.
- Implementação do deslocamento e da oscilação da embarcação.
- Desenvolvimento e organização do ambiente de demonstração.
- Integração do barco com o pinguim durante o embarque e desembarque.
- Ajustes e testes relacionados à sequência de interação.


## 7. Referências e fontes

STEMKOSKI, Lee; PASCALE, Michael. *Developing Graphics Frameworks with Python and OpenGL*. 1. ed. Boca Raton: CRC Press, 2022. DOI: [https://doi.org/10.1201/9781003181378](https://doi.org/10.1201/9781003181378).

- Livro acima: arquitetura do framework (grafo de cena, câmera, materiais, luzes) e abordagem de *shadow mapping* da seção 6.9, reimplementadas em `fw/`.
- Documentação do Pygame, PyOpenGL e NumPy.
- Texturas: nenhuma imagem de terceiros. `agua.png`, `madeira.png` e `neve.png` foram geradas por `tools/gerar_texturas.py` (ruído procedural gerado em Python, antes da execução). Origem registrada em `imagens/LICENCAS.txt`.

## 8. Declaração de uso de inteligência artificial

**Ferramenta:** Claude (Anthropic).

**Finalidade:** apoio à programação, à depuração, à elaboração dos testes e à documentação.

**Trechos desenvolvidos ou revisados com apoio da ferramenta:**

| Arquivos | Uso da IA |
|---|---|
| `fw/` (todos os arquivos) | Geração inicial do código e revisão, a partir da arquitetura do livro |
| `fw/shaders.py`, `fw/renderer.py` | Geração e revisão dos shaders e do shadow mapping (PCF, *bias*, *polygon offset*) |
| `cena/pinguim.py`, `cena/barco.py`, `cena/ambiente.py` | Geração inicial dos modelos e das animações; ajustes e testes feitos pelos integrantes |
| `cena/interacao.py`, `cena/utils_anim.py` | Geração e revisão da máquina de estados e das funções de interpolação |
| `tests/`, `tools/` | Geração dos testes e dos scripts auxiliares |
| `README.md` | Redação e revisão da documentação |

Os integrantes revisaram, executaram e adaptaram o código gerado, e são responsáveis por ele e capazes de explicar seu funcionamento. O uso da ferramenta não dispensou a revisão nem o estudo dos conceitos.

## 9. Shaders, atributos e uniforms

Os shaders estão em `fw/shaders.py` (GLSL 3.30 core) e são compilados em `fw/renderer.py` (`Programa`). A renderização usa **dois programas**, um para cada passe do *shadow mapping*.

### Atributos de vértice (layout intercalado: posição, normal, UV)

| Atributo | Location | Uso |
|---|---|---|
| `vertexPosition` | 0 | Posição do vértice (vec3) |
| `vertexNormal` | 1 | Normal, usada na iluminação (vec3) |
| `vertexUV` | 2 | Coordenada de textura (vec2) |

Os atributos são enviados em `Geometry._enviar()` (`fw/geometry.py`).

### Programa principal (passe 2: cor)

**Vertex shader** (`VERTEX_PRINCIPAL`): leva o vértice ao espaço do mundo, calcula a posição na tela, transforma a normal e calcula a posição do fragmento no espaço da luz.

| Uniform | Função |
|---|---|
| `modelMatrix` | Espaço do objeto para o espaço do mundo (inclui a hierarquia do grafo de cena) |
| `viewMatrix` | Mundo para o espaço da câmera (inversa da matriz da câmera) |
| `projectionMatrix` | Projeção em perspectiva |
| `normalMatrix` | Transposta da inversa de `mat3(modelMatrix)`, para transformar normais corretamente, inclusive com escala não uniforme |
| `lightMatrix` | Projeção ortográfica x visão da luz; leva o fragmento ao espaço da luz (usada para consultar o shadow map) |
| `repeatUV` | Fator de repetição das coordenadas de textura |

**Fragment shader** (`FRAGMENT_PRINCIPAL`): aplica o modelo de Phong (ambiente + difusa + especular), combina cor e textura e atenua a luz direta nas regiões em sombra.

| Uniform | Função |
|---|---|
| `baseColor`, `useTexture`, `tex` | Cor do material, indicador de textura e *sampler* da textura |
| `shininess`, `specularStrength` | Brilho e intensidade do componente especular |
| `ambientColor` | Luz ambiente |
| `lightColor`, `lightDir` | Cor e direção da luz direcional |
| `viewPos` | Posição da câmera, para o vetor de visão no cálculo especular |
| `shadowOn`, `shadowMap`, `shadowStrength`, `shadowBias` | Ativação do shadow map, *sampler* de profundidade, intensidade da sombra e *bias* |

### Programa de profundidade (passe 1: shadow map)

A cena é desenhada do ponto de vista da luz em um framebuffer só com textura de profundidade. O vertex shader (`VERTEX_PROFUNDIDADE`) usa apenas `vertexPosition` e os uniforms `modelMatrix` e `lightMatrix`. O fragment shader é vazio, pois apenas a profundidade é gravada.

### Sombreamento e sombra projetada

- **Sombreamento** (*shading*): variação da intensidade luminosa **na própria superfície**, conforme o ângulo entre a normal `N` e a direção da luz `L` (termo `max(dot(N, L), 0)`) e o componente especular. Não depende de outros objetos.
- **Sombra projetada** (*cast shadow*): região de uma superfície que **não recebe luz porque outro objeto está no caminho**. É calculada por *shadow mapping* em `calcSombra()`: o fragmento é levado ao espaço da luz e sua profundidade é comparada com a do shadow map; se estiver mais longe, está em sombra.
- **Ajustes do shadow mapping**: *bias* proporcional à inclinação da superfície (evita *shadow acne*), `glPolygonOffset` no passe de profundidade e PCF 3x3 (bordas suaves).
- O shadow map é refeito **a cada quadro**, então as sombras do pinguim e do barco acompanham o movimento.

## 10. Testes

Para executar os testes da lógica de interação sem inicializar o contexto gráfico:

```bash
python -m tests.test_interacao_sem_gl
```

Os testes verificam a sequência dos estados, a dependência entre as ações dos personagens, a continuidade do movimento, a independência da taxa de quadros e o comportamento durante a pausa.

---

**Repositório:** https://github.com/LucasSouza-git/Pinguin_Barco_Computa-o_Grafica
