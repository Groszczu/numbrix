import os
import itertools
import math
import pysat
from pysat import solvers


def read_board(input_file):
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
        n = len(board)
        
        self.board = board
        self.rows = round(math.sqrt(n))
        self.n = n
        self.all_possible_values = range(1, self.n + 1)
        self.solver = solvers.Glucose3(with_proof=True)

    def decode_cell(self, encoded_cell):
        encoded_cell_abs = abs(encoded_cell)
        id = (encoded_cell_abs - 1) // self.n + 1
        value = encoded_cell_abs - (id - 1) * self.n
        return id, value

    def encode_cell(self, id, value):
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
        for id in self.all_possible_values:
            clause = self.cell_has_assigned_value(id);
            self.solver.add_clause(clause)
        for id in self.all_possible_values:
            for clause in self.cell_is_unique(id):
                self.solver.add_clause(clause)

        for id1, id2 in itertools.product(self.all_possible_values, self.all_possible_values):
            if id1 != id2:
                for clause in self.cells_are_not_equal(id1, id2):
                    self.solver.add_clause(clause)
        for id in self.all_possible_values:
            neighbors = self.get_neighbors_ids(id)
            for clause in self.cells_neighbor_has_proceding_value(id, neighbors):
                self.solver.add_clause(clause)

        assumptions = []
        for id in self.all_possible_values:
            cell_value = self.get_cell_value(id)
            if cell_value != 0:
                assumptions.append(self.encode_cell(id, cell_value))
        
        print('Solvable?', self.solver.solve(assumptions))
        model = self.solver.get_model()
        self.solver.delete()

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
