import os
# from pysat.formula import CNF
import itertools
from pysat import solvers


def text_to_matrix(input_file):
    with open(input_file, 'r') as file:
        values = []
        rows = file.read().split('\n')
        id = 1
        for index, row in enumerate(rows):
            encoded_row = []
            for value in row.split():
                if value == '.':
                    encoded_value = 0
                else:
                    encoded_value = int(value)
                encoded_row.append((id, encoded_value))
                id += 1
            values.append(encoded_row)

        return values


class Puzzle:
    def __init__(self, board):
        col_len = len(board)
        for index, row in enumerate(board):
            row_len = len(row)
            if row_len != col_len:
                raise ValueError(
                    f'Puzzle\'s constructor\'s `board` argument should be two dimensional array with same number of columns and rows. Row with index {index} has length {row_len} and have length {col_len}'
                )

        self.board = board
        self.rows = col_len
        self.n = col_len * col_len
        self.all_possible_values = range(1, self.n + 1)
        self.solver = solvers.Glucose3()

    def encode_cell(self, id, value):
        return (id - 1) * self.n + value

    def cell_is_equal_to(self, id, value):
        return [self.encode_cell(id, value)]

    def cell_has_assigned_value(self, id):
        return [self.encode_cell(id, value) for value in self.all_possible_values]

    def cell_is_unique(self, id):
        cnf = []
        for value1 in range(1, self.n):
            for value2 in range(value1, self.n + 1):
                # one cell cannot have two values at once
                cnf.append([
                    -self.convert(id, value1),
                    -self.convert(id, value2)
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
        neighbors = []
        potential_neighbors = [id - 1, id + 1, id - self.rows, id + self.rows]
        for potential_neighbor_id in potential_neighbors:
            if potential_neighbor_id > 1 and potential_neighbor_id < self.n:
                neighbors.append(potential_neighbor_id)

        return neighbors

    def solve(self):
        for id in self.all_possible_values:
            self.solver.append_formula(self.cell_has_assigned_value(id))
        for id in self.all_possible_values:
            self.solver.append_formula(self.cell_is_unique(id))
        for r in itertools.product(self.all_possible_values, self.all_possible_values):
            print(r)


input = text_to_matrix('input.txt')
puzzle = Puzzle(input)
puzzle.solve()
