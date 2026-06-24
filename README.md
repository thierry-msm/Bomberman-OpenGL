# Bomberman 2D OpenGL

Este projeto consiste em um jogo multiplayer local estilo **Bomberman 2D** com perspectiva *top-down*, desenvolvido em **Python** utilizando **OpenGL Immediate Mode** para renderização gráfica e **Pygame** para gerenciamento de janela, eventos e entrada do teclado.

---

## 🎮 Funcionamento do Jogo

* **Objetivo:** Dois jogadores disputam em uma arena em grade. O objetivo é eliminar o oponente utilizando bombas posicionadas estrategicamente, enquanto destrói blocos para abrir caminho e obter vantagens. A partida é decidida em um formato de melhor de 5 rodadas (o primeiro a alcançar **5 vitórias** vence o jogo).
* **Power-ups:** Escondidos sob os blocos destrutíveis, oferecem melhorias cumulativas para o jogador que os coletar:
  * **Alcance (Flame):** Aumenta o raio de propagação das explosões das bombas.
  * **Quantidade (Bomb):** Permite plantar mais bombas simultaneamente na arena.
  * **Velocidade (Speed):** Aumenta a velocidade de movimento do personagem.
* **Controles:**
  * **Jogador 1:** Movimentação pelas teclas `W`, `A`, `S`, `D` e ação de plantar bomba com a barra de `Espaço`.
  * **Jogador 2:** Movimentação pelas teclas direcionais (`Setas`) e ação de plantar bomba com a tecla `Enter`.
  * **Interface/Menus:** `Enter` para avançar/confirmar, `R` para reiniciar (na tela de Game Over), `ESC` para sair ou retornar.

---

## 📁 Estrutura do Projeto

O projeto adota uma arquitetura estritamente modular dividida por responsabilidades:

* **`main.py`**: Ponto de entrada do jogo. Inicializa o Pygame, o contexto OpenGL, carrega os recursos principais e executa o loop principal único do jogo.
* **`settings.py`**: Constantes e configurações gerais do projeto (tamanho dos tiles, resolução de tela, FPS e cores do OpenGL).
* **`state_manager.py`**: Define a interface base para a máquina de estados (`BaseState` e `StateManager`).
* **`states/`**: Telas do jogo encapsuladas como estados individuais:
  * `start_screen.py`: Menu inicial com apresentação e instrução de início.
  * `match_playing.py`: A partida ativa (gameplay e atualização do cenário).
  * `round_score.py`: Tela intermediária mostrando o placar após cada rodada.
  * `game_over.py`: Tela final exibida quando um jogador atinge 5 vitórias.
* **`core/`**: Regras de negócio e lógica de física/estado da partida:
  * `game_state.py`: Mantém o estado ativo da rodada (mapa, jogadores, bombas, explosões e power-ups).
  * `collision.py`: Lógica de colisão física e delimitadores (AABB).
  * `input_handler.py`: Processamento de entradas discretas e contínuas de teclado.
  * `round_manager.py`: Controle das condições de término de cada rodada.
  * `score_manager.py`: Placar geral acumulado de vitórias.
* **`render/`**: Módulos dedicados à renderização em OpenGL:
  * `renderer.py`: Responsável por coordenar o desenho do cenário, das entidades e efeitos na arena.
  * `hud_renderer.py`: Renderização do painel superior de informações (HUD).
  * `text_renderer.py`: Conversão de texto em texturas OpenGL para exibição de texto na tela.
  * `texture_loader.py`: Carregamento de imagens do disco usando Pillow para a GPU.
  * `lighting.py`: Efeito de iluminação aditiva simulando luzes das explosões.
* **`entities/`**: Modelagem de entidades do domínio do jogo:
  * `player.py`: Jogador, movimentação e estado de vida.
  * `bomb.py`: Bomba, temporizador e lógica de bomb trap.
  * `explosion.py`: Definição de propagação de explosões em cruz.
  * `powerup.py`: Tipos e dados dos power-ups coletáveis.
  * `tilemap.py`: Tabuleiro da partida contendo paredes fixas, caixas destrutíveis e grama livre.
* **`assets/`**: Recursos estáticos (texturas PNG, fontes e áudio).

---

## 🛠️ Bibliotecas Utilizadas

* **Python 3**: Linguagem de programação base.
* **Pygame**: Criação da janela, captação de eventos de entrada (mouse/teclado) e controle de FPS.
* **PyOpenGL**: Renderização acelerada por hardware utilizando a API gráfica OpenGL em *Immediate Mode* (pipeline fixa, ex: `glBegin`/`glEnd`).
* **Pillow (PIL)**: Carregamento de imagens de textura do disco e sua conversão em bytes compatíveis com as funções do OpenGL.

---

## 💥 Funcionamento das Colisões

O sistema de colisão é inteiramente bidimensional e baseado em eixos alinhados (**AABB - Axis-Aligned Bounding Boxes**):
* **Bounding Boxes do Jogador:** Cada jogador possui uma caixa de colisão reduzida (tamanho $0.7 \times 0.7$ centralizado no tile de $1.0 \times 1.0$), o que garante um movimento fluido e facilita o deslize em cantos e corredores estreitos.
* **Colisão com o Mapa:** O motor de colisão projeta a posição do bounding box do jogador para o próximo frame e impede a movimentação caso haja sobreposição com blocos intransponíveis (paredes fixas ou destrutíveis).
* **Regra de Bomb Trap (Armadilha de Bomba):** Ao plantar uma bomba, o jogador está sobre ela. Para evitar que ele fique preso imediatamente, a colisão da bomba é desativada temporariamente para seu proprietário. No momento em que o jogador sai inteiramente do tile da bomba, a colisão é ativada em definitivo (`collision_locked = True`), bloqueando novas entradas dele e do oponente.

---

## 💡 Iluminação Dinâmica das Explosões

Como o projeto utiliza *Immediate Mode* e não faz uso de shaders customizados (GLSL), a iluminação dinâmica é simulada por meio de **blending (mesclagem de cores) em camadas**:
1. **Camada de Escuridão:** Um overlay retangular preto e semitransparente (`glColor4f(0, 0, 0, 0.45)`) é renderizado sobre toda a arena utilizando blend comum (`GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA`), criando uma atmosfera sombria.
2. **Luz Radial Aditiva:** O modo de mesclagem é alterado para blend aditivo (`GL_SRC_ALPHA, GL_ONE`). Para cada tile em chamas de uma explosão ativa, desenha-se um gradiente radial utilizando `GL_TRIANGLE_FAN`:
   * **Vértice central (origem):** Cor amarela/laranja quente e opaca (`glColor4f(1.0, 0.6, 0.15, 0.7 * intensidade)`).
   * **Vértices periféricos (borda do círculo):** Cor vermelha totalmente transparente (`alpha = 0.0`), produzindo uma atenuação suave que simula a luz irradiada pelo fogo.
3. **Atenuação Temporal:** O brilho e raio da iluminação diminuem gradativamente acompanhando o tempo restante de vida da explosão.

---

## 🎨 Texturas e Fontes

* **Texturas 2D:** Sprites para jogadores, blocos e bombas são lidos em formato PNG via **Pillow**, convertidos para RGBA e invertidos verticalmente (corrigindo a orientação espacial do OpenGL). É adotado o filtro `GL_NEAREST` para assegurar a nitidez das pixel-arts.
* **Controle de Estado de Textura:** O OpenGL opera como máquina de estados. Assim, a funcionalidade `GL_TEXTURE_2D` é explicitamente ativada (`glEnable`) apenas para desenhar sprites texturizados ou textos, sendo desativada (`glDisable`) antes do desenho de cores planas (como chão ou a camada de escuridão), evitando vazamento de texturas.
* **Renderização de Textos:** Para contornar a ausência de funções nativas de texto no OpenGL, o `TextRenderer` desenha os caracteres em uma `pygame.Surface` usando o motor de fontes do Pygame, converte essa superfície em bytes e a carrega na memória da GPU como uma textura OpenGL temporária para ser renderizada sobre a cena.

---

## 🔄 Máquina de Estados Finita (FSM)

O fluxo e as transições de tela são estruturados sob o padrão de design State Pattern:
* **`StateManager`:** Armazena o estado ativo e intermedia as transições chamando as rotinas `exit()` do estado que se encerra e `enter()` do novo estado que se inicia.
* **Estados do Jogo:**
  1. `START_SCREEN`: Apresentação inicial do jogo.
  2. `MATCH_PLAYING`: Lógica ativa da partida e controle das entidades em tempo real.
  3. `ROUND_SCORE`: Intermediário com placar atualizado de vitórias.
  4. `GAME_OVER`: Encerramento definitivo ao atingir 5 vitórias, permitindo nova rodada ou retorno ao menu.
* O loop principal em `main.py` delega continuamente o processamento de eventos, lógica e renderização do jogo ao estado ativo atual.
