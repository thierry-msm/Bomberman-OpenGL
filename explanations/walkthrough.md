# Walkthrough — Fase 3: Gameplay Principal

Nesta etapa, implementamos a lógica e a física completas da rodada do jogo, incluindo a movimentação dos jogadores com deslizamento nas paredes, o posicionamento automático das bombas no grid, a propagação de explosões em cruz (com destruição de tijolos e reação em cadeia), power-ups e a verificação automática de vitórias ou empates.

## O que foi implementado

### 1. Entidades do Jogo (Diretório `entities/`)
* **[entities/player.py](file:///Users/user/Projects/Bomberman-OpenGL/entities/player.py)**: `@dataclass` `Player` com id, posição flutuante no grid, velocidade, limite de bombas, alcance das explosões e estado de vida.
* **[entities/bomb.py](file:///Users/user/Projects/Bomberman-OpenGL/entities/bomb.py)**: `@dataclass` `Bomb` com posição no grid, temporizador (3s), alcance e a flag `collision_locked`.
* **[entities/explosion.py](file:///Users/user/Projects/Bomberman-OpenGL/entities/explosion.py)**: `@dataclass` `Explosion` armazenando a lista de coordenadas afetadas e o timer de vida (0.5s).
* **[entities/powerup.py](file:///Users/user/Projects/Bomberman-OpenGL/entities/powerup.py)**: `@dataclass` `PowerUp` com posição e tipo (`bomb_limit`, `bomb_range`, `speed`).
* **[entities/tilemap.py](file:///Users/user/Projects/Bomberman-OpenGL/entities/tilemap.py)**: Classe `TileMap` representada por listas de listas Python (13 colunas x 11 linhas). Gera automaticamente o mapa com bordas indestrutíveis, grelhas internas de pilares e 60% de tijolos destrutíveis aleatórios, garantindo segurança de spawn nos cantos para P1 e P2.

### 2. Física e Colisão
* **[core/collision.py](file:///Users/user/Projects/Bomberman-OpenGL/core/collision.py)**: 
  * Implementa caixa delimitadora AABB menor que 1.0 (tamanho 0.7) para permitir deslizamento suave dos jogadores.
  * Implementa a **regra do bomb trap**: o jogador dono da bomba pode passar por cima dela logo após plantá-la. Uma vez que ele saia completamente do tile da bomba, a colisão é ativada (`collision_locked = True`) e ela passa a bloqueá-lo.
  * Verifica colisões de jogadores com explosões (morte) e com power-ups (coleta).

### 3. Inputs e Controles
* **[core/input_handler.py](file:///Users/user/Projects/Bomberman-OpenGL/core/input_handler.py)**: Mapeia as teclas contínuas e calcula vetores de direção normalizados.
  * **Jogador 1 (Azul)**: W, A, S, D para andar e `ESPAÇO` para plantar bomba (discreto).
  * **Jogador 2 (Vermelho)**: Setas direcionais para andar e `ENTER` para plantar bomba (discreto).

### 4. Gerenciamento de Estado e Rodada (Diretório `core/`)
* **[core/game_state.py](file:///Users/user/Projects/Bomberman-OpenGL/core/game_state.py)**: Concentra e atualiza a simulação física: movimentação com deslizamento independente em X e Y, expiração de timers, propagação de explosões em cruz (interrompidas por blocos indestrutíveis e destruindo tijolos), reações em cadeia (detonação imediata de bombas adjacentes), surgimento aleatório de power-ups (25% ao quebrar tijolos) e aplicação de buffs.
* **[core/round_manager.py](file:///Users/user/Projects/Bomberman-OpenGL/core/round_manager.py)**: Analisa a integridade de vida de P1 e P2 a cada frame para decretar vitória da rodada ou empate caso ambos morram na mesma explosão.

### 5. Integração com a Interface
* **[states/match_playing.py](file:///Users/user/Projects/Bomberman-OpenGL/states/match_playing.py)**: Integrou o ciclo de vida completo de `GameState` no loop de jogo.
  * Desenha os blocos indestrutíveis (cinza volumoso), blocos destrutíveis (marrom texturizado), bombas (esferas pretas com pavio), chamas da explosão (laranja com centro amarelo incandescente), power-ups (coloridos com centro branco) e jogadores (Azul e Vermelho com detalhes de face).

---

## Como testar localmente

No terminal, execute o jogo:
```bash
venv/bin/python main.py
```

### Testes Recomendados
1. **Movimentação suave**: Controle ambos os jogadores no teclado simultaneamente. Verifique se eles deslizam suavemente pelos cantos dos corredores.
2. **Bomb Trap**: Plante uma bomba e certifique-se de que consegue andar sobre ela. Saia do tile e tente voltar; o jogador deve ser bloqueado.
3. **Explosões e Cadeia**: Coloque duas bombas próximas uma da outra. A explosão da primeira deve desencadear a detonação imediata da segunda.
4. **Power-ups**: Destrua blocos com bombas para revelar power-ups (Ciano: alcance, Magenta: bombas extras, Amarelo: velocidade) e colete-os para testar os efeitos.
5. **Condição de Vitória**: Elimine o oponente (ou suicide-se) para testar a transição automática de placares da rodada até o fim de jogo (5 vitórias).
