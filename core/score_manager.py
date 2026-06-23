class ScoreManager:
    """Gerencia a pontuação dos jogadores nas rodadas do Bomberman."""
    
    def __init__(self):
        self.player1_wins = 0
        self.player2_wins = 0
        self.target_wins = 5

    def add_win(self, player_id):
        """Adiciona uma vitória ao jogador correspondente."""
        if player_id == 1:
            self.player1_wins += 1
        elif player_id == 2:
            self.player2_wins += 1

    def has_champion(self):
        """Retorna True se algum jogador atingir a meta de vitórias."""
        return (
            self.player1_wins >= self.target_wins or
            self.player2_wins >= self.target_wins
        )

    def get_champion(self):
        """Retorna o ID do jogador campeão (1 ou 2), ou None se nenhum atingiu a meta."""
        if self.player1_wins >= self.target_wins:
            return 1
        if self.player2_wins >= self.target_wins:
            return 2
        return None
