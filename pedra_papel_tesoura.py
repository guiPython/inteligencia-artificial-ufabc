from typing import Tuple, TypeAlias, List, Literal
from random import choice

"""
Definicao de um jogo:

S(0): Estado incial.
Jogador(s): No estado S(n) indica qual o jogador do estado S(n + 1).
Acao(s): Sao as acoes disponiveis no estado S(n) para o(s) jogador(es).
Resultado(s, a): A transicao de estados com a aplicacao de a no estado s.
Terminal(s): Retorna se o jogo atingiu estado terminal.
Utilidade(s, p): Retorna o valor de utilidade para o jogador p no estado final s.
"""

Utilidade: TypeAlias = Literal[-1] | Literal[0] | Literal[1]
Jogador: TypeAlias = Literal["Um"] | Literal["Dois"]
Jogadas: TypeAlias = Literal["Pedra"] | Literal["Papel"] | Literal["Tesoura"]
Estado: TypeAlias = Tuple[Jogadas | None, Jogadas | None, Jogador] 

def inicio() -> Estado:
    return (None, None, choice(["Um", "Dois"]))

def proximo_jogador(estado: Estado) -> Jogador:
    _, _, jogador = estado
    return "Dois" if jogador == "Um" else "Um"

def acoes(estado: Estado) -> List[Jogadas]:
    return [] if eh_terminal(estado) else ["Pedra", "Papel", "Tesoura"]

def resultado(estado: Estado, jogada: Jogadas) -> Estado:
    if eh_terminal(estado):
        return estado

    jogada1, jogada2, jogador = estado
    if jogador == "Um":
        return (jogada, jogada2, "Dois")
    return (jogada1, jogada, "Um")

def eh_terminal(estado: Estado) -> bool:
    jogada1, jogada2, _ = estado
    return jogada1 is not None and jogada2 is not None

def jogadas_vencedoras_para(jogador: Jogador) -> List[Tuple[Jogadas, Jogadas]]:
    vencedoras_para_jogador_um: List[Tuple[Jogadas, Jogadas]] = [
        ("Papel", "Pedra"), 
        ("Pedra", "Tesoura"), 
        ("Tesoura", "Papel")]
    
    if jogador == "Um":
        return vencedoras_para_jogador_um
    return [(y, x) for x, y in vencedoras_para_jogador_um]

def utilidade(estado: Estado, jogador: Jogador) -> Utilidade | None:
    if not eh_terminal(estado): return None

    jogada1, jogada2, _ = estado
    if jogada1 == jogada2: return 0
    return 1 if (jogada1, jogada2) in jogadas_vencedoras_para(jogador) else -1