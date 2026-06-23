# Gerenciador de Estados do Jogo

class BaseState:
    """Classe base para todos os estados (telas) do jogo."""
    
    def enter(self, game):
        """Chamado quando o jogo entra neste estado."""
        pass

    def exit(self, game):
        """Chamado quando o jogo sai deste estado."""
        pass

    def handle_event(self, event, game):
        """Trata eventos discretos do Pygame (teclado, cliques, etc.)."""
        pass

    def update(self, dt, game):
        """Atualiza a lógica interna do estado a cada frame."""
        pass

    def render(self, game):
        """Renderiza os elementos deste estado usando OpenGL."""
        pass


class StateManager:
    """Gerencia a transição e delegação de funções para o estado ativo."""
    
    def __init__(self):
        self.current_state = None

    def change_state(self, new_state, game):
        """Realiza a transição segura entre estados do jogo."""
        if self.current_state:
            self.current_state.exit(game)
        self.current_state = new_state
        if self.current_state:
            self.current_state.enter(game)
