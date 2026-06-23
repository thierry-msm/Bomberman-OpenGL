from dataclasses import dataclass

@dataclass
class RoundResult:
    winner_id: int | None
    is_draw: bool
    message: str

def check_round_end(players):
    """
    Analisa o estado de vida dos jogadores.
    Retorna um objeto RoundResult se a rodada encerrou (vitória ou empate),
    ou None se a rodada ainda deve continuar (ambos vivos).
    """
    p1 = players.get(1)
    p2 = players.get(2)
    
    if not p1 or not p2:
        return None

    # Caso 1: Ambos mortos (Empate)
    if not p1.alive and not p2.alive:
        return RoundResult(
            winner_id=None,
            is_draw=True,
            message="Empate! Ambos foram eliminados na explosão."
        )
        
    # Caso 2: P1 vivo e P2 morto (Vitória do Jogador 1)
    if p1.alive and not p2.alive:
        return RoundResult(
            winner_id=1,
            is_draw=False,
            message="Jogador 1 venceu a rodada!"
        )
        
    # Caso 3: P2 vivo e P1 morto (Vitória do Jogador 2)
    if not p1.alive and p2.alive:
        return RoundResult(
            winner_id=2,
            is_draw=False,
            message="Jogador 2 venceu a rodada!"
        )

    # Caso 4: Ambos vivos (A rodada continua)
    return None
