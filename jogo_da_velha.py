from typing import TypeAlias, List, Tuple, Literal
from random import choice
from itertools import chain

"""
Definicao de um jogo:

S(0): Estado incial.
Jogador(s): No estado S(n) indica qual o jogador do estado S(n + 1).
Acao(s): Sao as acoes disponiveis no estado S(n) para o(s) jogador(es).
Resultado(s, a): A transicao de estados com a aplicacao de a no estado s.
Terminal(s): Retorna se o jogo atingiu estado terminal.
Utilidade(s, p): Retorna o valor de utilidade para o jogador p no estado final s.
"""

Jogador: TypeAlias = Literal['X'] | Literal['O']
Utilidade: TypeAlias = Literal[-1] | Literal[0] | Literal[1]
Tabuleiro: TypeAlias = List[List[Jogador | None]]
Estado: TypeAlias = Tuple[Tabuleiro, Jogador]
Terminal: TypeAlias = Tuple[Jogador | None, bool]
Acao: TypeAlias = Tuple[int, int]

def inicio() -> Estado:
    tabuleiro: Tabuleiro = [[None, None, None] for _ in range(3)]
    return (tabuleiro, choice(['X', 'O']))

def proximo_jogador(estado: Estado) -> Jogador:
    return 'X' if estado[1] == 'O' else 'O'

def acoes(estado: Estado) -> List[Acao]:
    tabuleiro, _ = estado
    return [(x, y) for x in range(3) for y in range(3) if tabuleiro[x][y] is None]

def resultado(estado: Estado, acao: Acao) -> Estado | None:
    tabuleiro, jogador = estado
    x, y = acao
    if tabuleiro[x][y] is not None: return None
    elif jogador == 'X': tabuleiro[x][y] = 'X'
    else:tabuleiro[x][y] = 'O'
    return (tabuleiro, 'X' if jogador == 'X' else 'O')

def linha_eh_terminal(linha: List[Jogador | None]) -> Terminal:
    if None in linha: return (None, False)
    elif linha.count('X') == 3: return ('X', True)
    elif linha.count('O') == 3: return ('O', True)
    return (None, True)

def eh_terminal(estado: Estado) -> Terminal:
    tabuleiro, _ = estado
    tabuleiro_transposto = list(zip(*tabuleiro))
    diagonal: List[Jogador | None] = [tabuleiro[x][x] for x in range(3)]
    outra: List[Jogador | None] = [tabuleiro[x][2 - x] for x in range(3)]

    for linha in [*tabuleiro, *tabuleiro_transposto, diagonal, outra]:
        vencedor, eh = linha_eh_terminal(linha)
        if eh and vencedor is not None: return (vencedor, True)

    return (None, False) if None in chain.from_iterable(tabuleiro) else (None, True)

def utilidade(estado: Estado, jogador: Jogador) -> Utilidade:
    vencedor, terminal = eh_terminal(estado)
    if not terminal: return 0
    if vencedor is None: return 0

    _, jogador = estado
    return 1 if vencedor == jogador else -1