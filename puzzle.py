import os
import itertools
import math
import pysat
from pysat import solvers



def read_board(input_file):
    '''
    Reads board from file and transform it into
    list of tuples `(id, value)` where `id` is an index of the cell starting from 1.
    If cell has no associated number with itself it's value will be set to 0.

    Returns: list of tuples shaped `(id, value)`.

    Examples:

        >>> cat input_file.txt
            1 . .
            6 5 4
            7 . .

        >>> read_board('input_file.txt')
            [(1, 1), (2, 0), (3, 0), (4, 6), (5, 5), (6, 4), (7, 7), (8, 0), (9, 0)]
    '''
    with open(input_file, 'r') as file:
        values = []
        rows = file.read()
        id = 1
        for value in rows.split():
            if value == '.':
                encoded_value = 0
            else:
                encoded_value = int(value)
            values.append((id, encoded_value))
            id += 1

        return values


class Puzzle:
    def __init__(self, board):
        '''
        Creates numbrix puzzle solver associated with given `board`.
        Board should be a square - square root of it's length should be natural number.
        Valid board's sizes: 1, 4, 9, 16...

        Args:

            board (list((int, int))): List of cells' tuples

        '''
        n = len(board)
        
        self.board = board
        self.rows = round(math.sqrt(n))
        self.n = n
        self.all_possible_values = range(1, self.n + 1)

    def decode_cell(self, encoded_cell):
        encoded_cell_abs = abs(encoded_cell)
        id = (encoded_cell_abs - 1) // self.n + 1
        value = encoded_cell_abs - (id - 1) * self.n
        return id, value

    def encode_cell(self, id, value):
        '''
        every cell and value associated with it can be represented by a range of numbers
        for example:
        if cell with index (id) 1 is filled with number 1
        we encode that into 1, because: (1 - 1) * n + 1
        if cell with index (id) 1 is filled with number 2
        we encode that into 2, because: (1 - 1) * n + 2
        and so on - so cell with index 1 can be encoded into values from 1 to n,
        cell with index 2 can be encoded into valuses from n + 1 to 2n,
        cell with index 3 can be encoded into valuses from 2n + 1 to 3n...

        Args:

            id: (int): id (1-based index) of the cell

            value: (int): value assigned to the cell. Value should never be grater than length of the board passed to constructor (`self.n`)

        Examples:

            >>> board = [(1, 0), ...] # board of length 81
            >>> puzzle = Puzzle(board)
            >>> puzzle.encode_cell(1, 1)
                1
            >>> puzzle.encode_cell(9, 42) # means that cell with index 9 has value 42
                690
                
        '''
        return (id - 1) * self.n + value

    def cell_is_equal_to(self, id, value):
        return [self.encode_cell(id, value)]

    def cell_has_assigned_value(self, id):
        return [self.encode_cell(id, value) for value in self.all_possible_values]

    def get_cell_value(self, id):
        for cell in self.board:
            if cell[0] == id:
                return cell[1]
        return None

    def cell_is_unique(self, id):
        cnf = []
        for value1 in range(1, self.n):
            for value2 in range(1, self.n):
                # one cell cannot have two values at once
                if value1 != value2:
                    cnf.append([
                        -self.encode_cell(id, value1),
                        -self.encode_cell(id, value2)
                    ])

        return cnf

    def cells_are_not_equal(self, id1, id2):
        cnf = []
        for value in self.all_possible_values:
            # two cells cannot have same value
            cnf.append([
                -self.encode_cell(id1, value),
                -self.encode_cell(id2, value)
            ])

        return cnf

    def cells_neighbor_has_proceding_value(self, id, neighbors):
        cnf = []
        for value in range(1, self.n):
            clause = [-self.encode_cell(id, value)]
            for neighbor_id in neighbors:
                clause.append(self.encode_cell(neighbor_id, value + 1))
            cnf.append(clause)

        return cnf

    def get_neighbors_ids(self, id):
        def in_same_row(id1, id2):
            res = (id1 - 1) // self.rows == (id2 - 1) // self.rows
            return res
        def in_same_col(id1, id2):
            res = id1 % self.rows == id2 % self.rows
            return res

        neighbors = []
        potential_neighbors = [id - 1, id + 1, id - self.rows, id + self.rows]
        for potential_neighbor_id in potential_neighbors:
            if (potential_neighbor_id >= 1 and
                potential_neighbor_id <= self.n and
                (in_same_col(id, potential_neighbor_id) or in_same_row(id, potential_neighbor_id))):
             
                neighbors.append(potential_neighbor_id)

        return neighbors

    def format_result(self, result):
        res = ''
        for id, value in result:
            res += str(value) + '\t'
            if (id % self.rows == 0):
                res += '\n'
        return res


    def solve(self):
        solver = solvers.Glucose3()
        for id in self.all_possible_values:
            clause = self.cell_has_assigned_value(id);
            solver.add_clause(clause)
        for id in self.all_possible_values:
            for clause in self.cell_is_unique(id):
                solver.add_clause(clause)

        for id1, id2 in itertools.product(self.all_possible_values, self.all_possible_values):
            if id1 != id2:
                for clause in self.cells_are_not_equal(id1, id2):
                    solver.add_clause(clause)
        for id in self.all_possible_values:
            neighbors = self.get_neighbors_ids(id)
            for clause in self.cells_neighbor_has_proceding_value(id, neighbors):
                solver.add_clause(clause)

        assumptions = []
        for id in self.all_possible_values:
            cell_value = self.get_cell_value(id)
            if cell_value != 0:
                assumptions.append(self.encode_cell(id, cell_value))
        
        print('Solvable?', solver.solve(assumptions))
        model = solver.get_model()
        solver.delete()

        result = []
        for encoded_cell_value in model:
            if encoded_cell_value > 0:
                result.append(self.decode_cell(encoded_cell_value))

        return result



if __name__ == '__main__':
    input = read_board('input.txt')
    puzzle = Puzzle(input)
    print('Input board')
    print(puzzle.format_result(puzzle.board))
    result = puzzle.solve()
    print('Result board')
    print(puzzle.format_result(result))
