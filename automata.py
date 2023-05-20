import json
"""
    Example of finite automata:
    states = {0, 1, 2, 3, 4, 5, 6}
    litery = {'a', 'b', 'c'}
    accept = {0, 2, 4}
    start=0
    moves={
    (0, 'a'): 1, (0, 'b'): 3, (0, 'c'): 5,
    (1, 'a'): 0, (1, 'b'): 6, (1, 'c'): 6,
    (2, 'a'): 1, (2, 'b'): 3, (2, 'c'): 5,
    (3, 'a'): 6, (3, 'b'): 2, (3, 'c'): 6,
    (4, 'a'): 1, (4, 'b'): 3, (4, 'c'): 5,
    (5, 'a'): 6, (5, 'b'): 6, (5, 'c'): 4,
}

automata_object = Automata(symbols=litery, states=states, moves=moves, start=start, accept=accept)
"""

class Automata():

    def __init__(self, symbols: set, states: set, moves: dict, start: str, accept: set) -> None:
        self.symbols = symbols
        self.states = states
        self.moves = moves
        self.start = start
        self.accept = accept
    
    # Solves the word and returns a tuple (accepted, end_state, moves)
    def solve(self, word: str) -> tuple:
        state = self.start
        moves = []

        # Moves through the word and checks if the moves are valid
        for letter in word:
            if (state, letter) not in self.moves:
                return False, moves
            state = self.moves[(state, letter)]
            moves.append((state, letter))

        # Check if the end state is an accept state
        if state in self.accept:
            return True, 'q' + str(state), moves
        return False, 'q' + str(state), moves


def print_result(accepted: bool, end_state: str, moves: list) -> None:
    if accepted:
        print(f'Machine accepted the word. End state: {end_state}')
    else:
        print(f'Machine did not accept the word. End state: {end_state}')
    print('Moves:')
    for move in moves:
        print(f'{move[1]} -> q{move[0]}', end=', ')
    print()


# Zapisanie automatów do danego pliku
def save_automat_to_file(filename: str, automata: Automata) -> None:
    states = {}
    letters = {}
    move = {}
    accepts = {}
    states['states'] = list(automata.states)
    letters['letters'] = list(automata.symbols)
    move = list(automata.moves.items())
    start = automata.start
    accepts['accept'] = list(automata.accept)
    automat_array = [states, letters, move, start, accepts]
    
    with open(filename, 'w') as file:
        json.dump(automat_array, file)


# Stworzenie automatów z danego pliku
def load_automat_from_file(filename: str) -> Automata:
    with open(filename, 'r') as file:
        automat_array = json.load(file)

    states = set(automat_array[0]['states'])
    letters = set(automat_array[1]['letters'])
    start = automat_array[3]
    accept = set(automat_array[4]['accept'])
    move_array = automat_array[2]

    # Przekształcenie listy przemieszczeń na słownik
    moves = automat_array[2]
    move = {}
    for i in moves:
        i[0] = tuple(i[0])
        move[i[0]] = i[1]

    return Automata(symbols=letters, states=states, moves=move, start=start, accept=accept)