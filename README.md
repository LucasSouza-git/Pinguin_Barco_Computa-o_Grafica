# Pinguim e Barco a Motor — Computação Gráfica

Trabalho prático desenvolvido para a disciplina de Computação Gráfica do curso de Ciência da Computação da UNIPAC Barbacena, período 2026/02.

## 1. Identificação

| Integrante | Tema sorteado |
|---|---|
| Aluno 1 | Pinguim de brinquedo |
| Aluno 2 | Barco a motor |

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

O desenvolvimento da aplicação utiliza o framework gráfico apresentado no livro *Developing Graphics Frameworks with Python and OpenGL*, de Lee Stemkoski e Michael Pascale.

O framework foi desenvolvido utilizando Python e OpenGL, oferecendo uma estrutura organizada para a construção e renderização de cenas tridimensionais. Seus componentes permitem a criação de objetos geométricos, organização hierárquica dos elementos, aplicação de materiais e texturas, configuração de câmeras, iluminação e renderização.

No projeto, o framework foi utilizado como base para a construção dos modelos tridimensionais do pinguim e do barco, além da composição do ambiente e da implementação dos recursos gráficos exigidos pelo trabalho.

Entre os principais conceitos e componentes utilizados estão:

- **Scene Graph:** organização hierárquica dos objetos e de suas partes.
- **Geometry:** construção dos modelos por composição de formas geométricas.
- **Transformações geométricas:** translação, rotação e escala dos objetos.
- **Materials e Textures:** definição da aparência e aplicação de imagens às superfícies.
- **Camera:** configuração da visualização em perspectiva.
- **Lighting:** aplicação de iluminação direcional e materiais sensíveis à luz.
- **Shaders:** processamento dos vértices e cálculo da aparência das superfícies.
- **Shadow Mapping:** técnica utilizada para produzir sombras projetadas na cena.

A estrutura do framework foi adaptada e integrada à aplicação para atender às necessidades específicas da cena e da interação entre os personagens.

A implementação utiliza os conceitos apresentados nos capítulos do livro, especialmente os relacionados à construção do framework, transformações geométricas, texturas, iluminação e sombras.

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

| Arquivo / diretório | Responsabilidade |
|---|---|
| `main.py` | Inicialização da aplicação |
| `fw/` | Componentes do framework gráfico |
| `cena/pinguim.py` | Modelagem do pinguim |
| `cena/barco.py` | Modelagem do barco |
| `cena/ambiente.py` | Construção do ambiente |
| `cena/interacao.py` | Máquina de estados e coordenação das ações |
| `cena/transformacoes.py` | Operações de transformação geométrica |
| `cena/app.py` | Controle da aplicação, câmera e animação |
| `fw/shaders.py` | Shaders utilizados na renderização |
| `fw/renderer.py` | Processo de renderização e shadow mapping |
| `tools/gerar_texturas.py` | Geração dos recursos de textura |
| `tests/test_interacao_sem_gl.py` | Testes da lógica de interação |

## 6. Contribuições individuais

### Aluno 1 — Modelagem e animação do pinguim

Responsável pelo desenvolvimento do modelo tridimensional do pinguim, incluindo:

- Construção do personagem por composição de formas geométricas.
- Organização hierárquica das partes do modelo.
- Implementação dos movimentos de caminhada, aceno e salto.
- Integração do personagem à sequência de interação.
- Ajustes e testes relacionados à movimentação do pinguim.

### Aluno 2 — Modelagem do barco e integração da cena

Responsável pelo desenvolvimento do barco e pela integração dos elementos da cena, incluindo:

- Construção do modelo tridimensional do barco.
- Implementação do deslocamento e da oscilação da embarcação.
- Desenvolvimento e organização do ambiente de demonstração.
- Integração do barco com o pinguim durante o embarque e desembarque.
- Ajustes e testes relacionados à sequência de interação.

**Observação:** as atribuições acima representam uma proposta de divisão. Os integrantes devem confirmar e ajustar as responsabilidades conforme as atividades efetivamente realizadas.

## 7. Referências

STEMKOSKI, Lee; PASCALE, Michael. *Developing Graphics Frameworks with Python and OpenGL*. 1. ed. Boca Raton: CRC Press, 2022. DOI: https://doi.org/10.1201/9781003181378.

As texturas utilizadas no projeto foram geradas por meio do script `tools/gerar_texturas.py`. As informações de origem e licenciamento dos recursos estão disponíveis em `imagens/LICENCAS.txt`.

## 8. Declaração de uso de inteligência artificial

Durante o desenvolvimento do projeto, ferramentas de inteligência artificial foram utilizadas pontualmente como apoio ao processo de aprendizagem e desenvolvimento.

- **Ferramenta utilizada:** Claude (Anthropic).
- **Finalidade:** esclarecimento de dúvidas técnicas, auxílio na compreensão de conceitos de programação gráfica e orientação na identificação de erros durante o desenvolvimento.
- **Utilização:** apoio consultivo durante o desenvolvimento, sem substituir a implementação, os testes e a validação realizados pelos integrantes.
- **Responsabilidade:** os integrantes são responsáveis pelo código final, pela verificação do funcionamento da aplicação e pela compreensão dos recursos gráficos implementados.

## 9. Shaders, atributos e uniforms

A aplicação utiliza shaders desenvolvidos em GLSL para realizar a renderização dos objetos tridimensionais.

### Atributos de vértice

- `vertexPosition`: posição do vértice.
- `vertexNormal`: vetor normal utilizado nos cálculos de iluminação.
- `vertexUV`: coordenadas utilizadas para aplicação de texturas.

### Vertex shader

O vertex shader realiza as transformações dos vértices e prepara os dados necessários para a etapa de fragmentação.

Entre os principais uniforms utilizados estão:

- `modelMatrix`: transforma o objeto para o espaço do mundo.
- `viewMatrix`: transforma os objetos de acordo com a posição da câmera.
- `projectionMatrix`: aplica a projeção em perspectiva.
- `normalMatrix`: transforma corretamente os vetores normais.
- `lightMatrix`: transforma os pontos para o espaço da fonte de luz.
- `repeatUV`: controla a repetição das coordenadas de textura.

### Fragment shader

O fragment shader utiliza o modelo de iluminação de Phong para calcular a aparência das superfícies, considerando componentes ambientais, difusas e especulares.

Também realiza a combinação da cor base do material com a textura aplicada ao objeto.

### Sombreamento e sombras projetadas

O sombreamento corresponde à variação de intensidade luminosa sobre uma superfície, considerando sua orientação em relação à fonte de luz.

A sombra projetada ocorre quando um objeto bloqueia a iluminação que atingiria outra superfície.

O projeto utiliza shadow mapping para calcular as sombras projetadas, com comparação de profundidade e técnicas de suavização.

## 10. Testes

Para executar os testes da lógica de interação sem inicializar o contexto gráfico:

```bash
python -m tests.test_interacao_sem_gl
```

Os testes verificam a sequência dos estados, a dependência entre as ações dos personagens, a continuidade do movimento, a independência da taxa de quadros e o comportamento durante a pausa.

---

**Repositório:** https://github.com/LucasSouza-git/Pinguin_Barco_Computa-o_Grafica
