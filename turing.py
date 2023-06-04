from json import load, dump

"""
    Example of a turing machine:

    states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'qa', 'qr'}
    alfabet = {'a', '.a', '/a', False}
    input_alfabet = {'a'}
    start = 'q0'
    accept = {'qa'}
    reject = {'qr'}
    moves = {
    #   Not putting a value in the dict means that the move is invalid and the machine will reject the word
    #   but you can still put value from reject to new_state to reject the word implicitly
    #   From   Read     Write    Move      To
    #   State, value,  new_val, direction, new_state
        ('q0', 'a'):    ('.a',   'right',  'q1'),
        ('q1', '/a'):   (False,  'right',  'q1'),
        ('q1', 'a'):    (False,  'left',   'q2'),
        ('q1', False):  (False,  'left',   'qa'),
        ('q2', '/a'):   (False,  'left',   'q2'),
        ('q2', '.a'):   (False,  'left',   'q3'),
        ('q3', '/a'):   (False,  'right',  'q3'),
        ('q3', 'a'):    (False,  'right',  'q4'),
        ('q3', '.a'):   (False,  'right',  'q4'),
        ('q3', False):  (False,  'left',   'q6'),
        ('q4', '/a'):   (False,  'right',  'q4'),
        ('q4', 'a'):    ('/a',   'right',  'q5'),
        ('q5', '/a'):   (False,  'right',  'q5'),
        ('q5', 'a'):    ('/a',   'right',  'q3'),
        ('q6', '/a'):   (False,  'left',   'q6'),
        ('q6', 'a'):    (False,  'left',   'q6'),
        ('q6', '.a'):   (False,  'right',  'q1')
    }
    
    zad1_tape = tape_input(input_alfabet, '1')

    turing_object = Turing_Machine(
    tape=zad1_tape, 
    moves=moves, 
    states=states, 
    alfabet=alfabet, 
    input_alfabet=input_alfabet,
    start=start, 
    accept=accept, 
    reject=reject, 
    )
"""


class Tape():
    valid_moves = {'left', 'right'}
    def __init__(self, tape = "") -> None:
        self.pos = 0
        self.tape = []
        for letter in tape:
            self.tape.append(letter)


    # Moves the tape left or right
    def move_tape(self, direction: str) -> None:
        if direction not in Tape.valid_moves:
            print('Invalid move, move "left" or "right"')
        elif direction == 'left' and self.pos > 0:
            self.pos -= 1
        elif direction == 'right' and self.pos < len(self.tape):
            self.pos += 1


class Turing_Machine():
    def __init__(
            self,  
            states: dict, 
            alfabet: set, 
            input_alfabet: set, 
            moves: dict,
            start: str, 
            accept: set, 
            reject: set,
            tape = Tape()
            ) -> None:
        self.curr_tape = tape
        self.states = states
        self.alfabet = alfabet
        self.input_alfabet = input_alfabet
        self.moves = moves
        self.current_state = start
        self.accept = accept
        self.reject = reject
    

    # Solves the word and returns a boolean if the word was accepted or not
    def solve(self, print_status = False) -> bool:
        while True:
            # Wykonuje ruch w maszynie Turinga
            # move = False means that the move can't be done
            move = self.__make_move(print_status)
            if self.current_state in self.accept:
                if print_status:
                    print(f"End tape: {self.curr_tape.tape}, End position: {self.curr_tape.pos}")
                return True
            if self.current_state in self.reject or move == False:
                if print_status:
                    print(f"End tape: {self.curr_tape.tape}, End position: {self.curr_tape.pos}")
                return False
    

    # Insert a new tape to the machine
    def insert_new_tape(self, tape: Tape) -> None:
        self.curr_tape = tape


    # Makes a move in the turing machine
    def __make_move(self, print_status: bool) -> bool:
        value = self.__read_value()
        if value not in self.alfabet:
            return False
        state = self.current_state
        if print_status:
            print(value, state)
            print(self.curr_tape.tape, self.curr_tape.pos)
            print()
        try:
            print(self.moves[(state, value)])
            new_value, move_dir, new_state = self.moves[(state, value)]
        except KeyError:
            return False
        if new_value != False:
            self.__change_value(new_value)
        self.curr_tape.move_tape(move_dir)
        self.current_state = new_state
        return True
    

    # Read the value from the current cell
    def __read_value(self):
        # If the move is invalid return False
        try:
            return self.curr_tape.tape[self.curr_tape.pos]
        except Exception:
            return False
    

    # Change the value of the current cell
    def __change_value(self, value: str) -> None:
        self.curr_tape.tape[self.curr_tape.pos] = value


# Function that loads the Tape from the user input and checks if it's valid
def tape_input(input_alfabet: set, zad: str):
    while True:
        tape = input(f'Podaj tasme maszyny turinga do zadania {zad}: ')
        # Check if the tape is valid
        # if yes return the tape
        # if not ask for a new tape (input)
        if all(letter in input_alfabet for letter in tape):
            break
        else:
            print('Tasma nie jest poprawna')
    return Tape(tape)


# Save the turing machine to a json file
def save_turing_to_file(turing: Turing_Machine, filename: str) -> None:
    states = {}
    alfabet = {}
    move = {}
    accepts = {}
    input_alfabet = {}
    reject = {}
    tape = {}
    tape['tape'] = ''
    for i in turing.curr_tape.tape:
        tape['tape'] += i
    states['states'] = list(turing.states)
    alfabet['alfabet'] = list(turing.alfabet)
    move['moves'] = list(turing.moves.items())
    start = turing.current_state
    accepts['accept'] = list(turing.accept)
    input_alfabet['input_alfabet'] = list(turing.input_alfabet)
    reject['reject'] = list(turing.reject)
    turing_array = [states, alfabet, start, accepts, input_alfabet, reject, move, tape]
    
    with open(filename, 'w') as file:
        dump(turing_array, file)


# Create a turing machine from a json file
def load_turing_from_file(filename: str) -> Turing_Machine:
    with open(filename, 'r') as file:
        turing_array = load(file)

    file_states = set(turing_array[0]['states'])
    file_alfabet = set(turing_array[1]['alfabet'])
    file_start = turing_array[2]
    file_accept = set(turing_array[3]['accept'])
    file_input_alfabet = set(turing_array[4]['input_alfabet'])
    file_reject = set(turing_array[5]['reject'])
    file_moves = turing_array[6]['moves']
    file_tape = turing_array[7]['tape']

    file_move = {}
    for i in file_moves:
        i[0] = tuple(i[0])
        file_move[i[0]] = i[1]

    return Turing_Machine(
        alfabet=file_alfabet, 
        states=file_states, 
        moves=file_move, 
        start=file_start, 
        accept=file_accept, 
        reject=file_reject,
        input_alfabet=file_input_alfabet,
        tape=Tape(file_tape)
        )


def zad1(print_status = False):
    states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'qa', 'qr'}
    alfabet = {'a', '.a', '/a', False}
    input_alfabet = {'a'}
    start = 'q0'
    accept = {'qa'}
    reject = {'qr'}
    moves = {
    #   From   Read     Write    Move      To
    #   State, value,   new_val, move_dir, new_state
        ('q0', 'a'):    ('.a',   'right',  'q1'),
        ('q0', False):  (False,  'left',   'qr'),
        ('q1', '/a'):   (False,  'right',  'q1'),
        ('q1', 'a'):    (False,  'left',   'q2'),
        ('q1', False):  (False,  'left',   'qa'),
        ('q2', '/a'):   (False,  'left',   'q2'),
        ('q2', '.a'):   (False,  'left',   'q3'),
        ('q3', '/a'):   (False,  'right',  'q3'),
        ('q3', 'a'):    (False,  'right',  'q4'),
        ('q3', '.a'):   (False,  'right',  'q4'),
        ('q3', False):  (False,  'left',   'q6'),
        ('q4', '/a'):   (False,  'right',  'q4'),
        ('q4', 'a'):    ('/a',   'right',  'q5'),
        ('q4', False):  (False,  'left',   'qr'),
        ('q5', '/a'):   (False,  'right',  'q5'),
        ('q5', 'a'):    ('/a',   'right',  'q3'),
        ('q5', False):  (False,  'left',   'qr'),
        ('q6', '/a'):   (False,  'left',   'q6'),
        ('q6', 'a'):    (False,  'left',   'q6'),
        ('q6', '.a'):   (False,  'right',  'q1')
    }
    
    zad1_tape = tape_input(input_alfabet, '1')

    zad1_turing = Turing_Machine(
    tape=zad1_tape, moves=moves, states=states, alfabet=alfabet, input_alfabet=input_alfabet,
    start=start, accept=accept, reject=reject, 
    )

    print(zad1_turing.solve(print_status=print_status))


if __name__ == "__main__":
    print('Turing Machine class file')
    zad1(print_status=True)
    turing = load_turing_from_file('turing.json')
    turing.solve(print_status=True)
    save_turing_to_file(turing, "zad1_out")
