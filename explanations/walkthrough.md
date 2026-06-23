# Walkthrough — Fase 2: Telas, Texto e Interface

Nesta etapa, implementamos com sucesso o renderizador de textos por textura OpenGL, o renderizador de HUD e enriquecemos visualmente todas as telas de transição com informações reais (título, instruções de controle, placares de rodada e final).

## O que foi implementado

### 1. Renderizador de Texto via OpenGL
* **[render/text_renderer.py](file:///Users/user/Projects/Bomberman-OpenGL/render/text_renderer.py)**: Utiliza `pygame.font.Font` para renderizar o texto em uma `pygame.Surface`, convertendo a imagem em bytes (`RGBA`) e carregando-a na GPU como uma textura OpenGL 2D temporária (`glTexImage2D`). O texto é desenhado em um quad (`GL_QUADS`) com coordenadas mapeadas corretamente para a projeção ortográfica 2D invertida do jogo. Para evitar vazamento de memória de GPU, a textura é deletada (`glDeleteTextures`) imediatamente após o desenho. Também inclui cache de fontes para máxima eficiência e suporte a alinhamento (`left`, `center`, `right`).

### 2. Renderizador da HUD
* **[render/hud_renderer.py](file:///Users/user/Projects/Bomberman-OpenGL/render/hud_renderer.py)**: Desenha uma barra superior cinza escuro com uma borda dourada fina (desativando texturas 2D via `glDisable(GL_TEXTURE_2D)` para desenhar geometria plana pura). Exibe os placares dinâmicos de cada jogador (P1 em azul, P2 em vermelho) nas extremidades da barra e o status centralizado utilizando o renderizador de texto.

### 3. Telas Enriquecidas com Textos e Controles
* **[states/start_screen.py](file:///Users/user/Projects/Bomberman-OpenGL/states/start_screen.py)**: Exibe o título grande do jogo, um divisor dourado semitransparente, a lista detalhada de controles de movimentação/bombas de cada jogador, e a instrução "Pressione ENTER para iniciar".
* **[states/round_score.py](file:///Users/user/Projects/Bomberman-OpenGL/states/round_score.py)**: Mostra quem venceu a rodada atual ou se foi empate, exibe painéis visuais cinzas translúcidos com o placar numérico de cada jogador lado a lado, e a instrução para continuar.
* **[states/game_over.py](file:///Users/user/Projects/Bomberman-OpenGL/states/game_over.py)**: Exibe o vencedor definitivo da partida, o placar final e as instruções para reiniciar (`R`) ou voltar ao menu inicial (`ESC`).

### 4. Integração no Jogo
* **[main.py](file:///Users/user/Projects/Bomberman-OpenGL/main.py)**: Integra o `TextRenderer` centralizado e o compartilha em todos os estados.
* **[states/match_playing.py](file:///Users/user/Projects/Bomberman-OpenGL/states/match_playing.py)**: Agora desenha o grid de fundo da arena de combate (verde oliva escuro), renderiza a HUD dinâmica no topo e fornece as instruções de teclas simuladas no centro da tela.

---

## Como testar localmente

No terminal, execute o jogo:
```bash
venv/bin/python main.py
```

### Controles de Simulação de Fluxo
* **Tela Inicial**: Pressione `ENTER` para iniciar o combate.
* **Arena da Partida (Verde/Cinza)**: 
  * Visualize a HUD no topo com os nomes dos jogadores e controles.
  * Pressione `1` para simular vitória do Jogador 1 (Azul).
  * Pressione `2` para simular vitória do Jogador 2 (Vermelho).
  * Pressione `3` para simular um empate.
* **Tela do Placar (Marrom)**: Veja o vencedor da rodada e o placar numérico atualizado. Pressione `ENTER` para retornar à partida.
* **Tela Final (Vermelho Escuro)**: Veja quem conquistou a vitória geral (ao alcançar 5 vitórias). Pressione `R` para jogar novamente ou `ESC` para voltar à tela inicial.
