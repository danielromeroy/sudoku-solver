import itertools as itt
import copy as c
import random as rd

INPUT_FILE = "data/sudoku_4_solutions"
MAX_SUDOKUS = 50000


class SudokuSolver:
    def __init__(self, init_status: list):
        self.solve_status = init_status
        self.possible_solutions = {}
        self.solved = False
        self.last_updated = ""
        self.intelligent_branching = False

    def compute_solutions(self):
        if self.last_updated != "":
            upd_row = int(self.last_updated[0])
            upd_col = int(self.last_updated[1])
            upd_subsq = self.get_subsq(self.last_updated)
            for i in range(1, 10):  # row
                for j in range(1, 10):  # col
                    if i == upd_row or \
                       j == upd_col or \
                       self.get_subsq(f"{i}{j}") == upd_subsq:
                        self.update_cell_solutions(row=i, col=j)
        else:
            for i in range(1, 10):  # row
                for j in range(1, 10):  # col
                    self.update_cell_solutions(row=i, col=j)

    def update_cell_solutions(self, row, col):
        if self.solve_status[row - 1][col - 1] == "X":
            row_values = self.solve_status[row - 1]
            row_values = list(set(row_values))
            if "X" in row_values:
                row_values.remove("X")

            col_values = [r[col - 1] for r in self.solve_status]
            col_values = list(set(col_values))
            if "X" in col_values:
                col_values.remove("X")

            subsq_values = []
            for m in range(1, 10):  # row
                for n in range(1, 10):  # col
                    if ((row - 1) // 3) == ((m - 1) // 3) and \
                            ((col - 1) // 3) == ((n - 1) // 3) and \
                            self.solve_status[m - 1][n - 1] != "X":
                        subsq_values.append(self.solve_status[m - 1][n - 1])
            subsq_values = list(set(subsq_values))

            forbidden_values = list(set(row_values + col_values + subsq_values))
            self.possible_solutions[f"{row}{col}"] = [str(m) for m in range(1, 10) if str(m) not in forbidden_values]
        else:
            self.possible_solutions[f"{row}{col}"] = []

    def has_unique_values(self):
        for values in self.possible_solutions.values():
            if len(values) == 1:
                return True
        return False

    def assign_unique_values(self):
        while self.has_unique_values():
            for cell in self.possible_solutions.keys():
                if len(self.possible_solutions[cell]) == 1:
                    row = int(cell[0])
                    col = int(cell[1])
                    self.solve_status[row - 1][col - 1] = self.possible_solutions[cell][0]
                    self.last_updated = cell
                    self.possible_solutions[cell] = []
                    self.check_solved()
                    if not self.solved:
                        self.compute_solutions()
                    break

    def check_solved(self):
        if "X" not in list(itt.chain(*self.solve_status)):
            self.solved = True

    def is_impossible(self):
        for solutions in self.possible_solutions.values():
            if len(solutions) > 0:
                return False
        return True

    def branch_solutions(self):
        branch_cell = self.choose_branch_cell()
        branched_solutions = []
        row = int(branch_cell[0])
        col = int(branch_cell[1])
        for solution in self.possible_solutions[branch_cell]:
            new_branch = c.deepcopy(self.solve_status)
            new_branch[row - 1][col - 1] = solution
            branched_solutions.append(new_branch)
        return branched_solutions

    def choose_branch_cell(self):
        value_amounts = list(set([len(values) for values in self.possible_solutions.values()]))
        candidate_cells = [cell for cell in self.possible_solutions.keys()
                           if len(self.possible_solutions[cell]) == value_amounts[1]]
        if not self.intelligent_branching:
            return rd.choice(candidate_cells)
        else:
            pass  # TODO: find least ocurring values in candidate cells

    def get_subsq(self, cell):
        row = int(cell[0])
        col = int(cell[1])
        return (row - 1) // 3, (col - 1) // 3

    def solution_to_string(self):
        return "\n".join([" ".join(row) for row in self.solve_status])

    def solution_to_string_forwebsite(self):
        string = self.solution_to_string()
        string = string.replace(" ", "")
        string = string.replace("X", ".")
        string = string.replace("\n", "")
        return string


def all_solved():
    global sudokus
    for solver in sudokus:
        if not solver.solved:
            return False
    return True


def remove_duplicates():
    global sudokus
    for i in reversed(range(0, len(sudokus))):
        test_solver = sudokus[i]
        # print(f"{sudokus=}")
        # print(f"{test_solver=}")
        for j in reversed(range(0, i)):
            if test_solver.solve_status == sudokus[j].solve_status:
                sudokus.pop(i)
                break


if __name__ == '__main__':
    with open(INPUT_FILE) as sudoku_file:
        init_sudoku_solve_status = [line.split() for line in sudoku_file]

    sudokus = [SudokuSolver(init_sudoku_solve_status)]
    # debug_count = 0
    while not all_solved():
        # debug_count += 1
        # print(f"{debug_count=} {len(sudokus)=}")
        if len(sudokus) > MAX_SUDOKUS:
            raise MemoryError("Amount of sudokus exceeded limit. Input sudoku is too vague.")
        sudoku = sudokus.pop()
        if not sudoku.solved:
            sudoku.compute_solutions()
            if sudoku.has_unique_values():
                sudoku.assign_unique_values()
                sudokus.append(sudoku)
            elif not sudoku.solved and not sudoku.is_impossible():
                sudokus.extend([SudokuSolver(solution) for solution in sudoku.branch_solutions()])
            elif sudoku.is_impossible() and not sudoku.solved:
                continue
        else:
            sudokus.insert(0, sudoku)
        remove_duplicates()

    # print(f"{len(sudokus)=}")

    for i, sudoku in enumerate(sudokus):
        print(f"Solution n {i + 1}:")
        print(sudoku.solution_to_string(), "\n")
