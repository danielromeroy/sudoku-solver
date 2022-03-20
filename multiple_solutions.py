import itertools as itt
import copy as c
import random as rd

INPUT_FILE = "data/sudoku_2_solutions"
MAX_SUDOKUS = 50000


class SudokuSolver:
    def __init__(self, init_status: list):
        self.solve_status = init_status
        self.possible_solutions = {}
        self.solved = False
        self.last_updated = []
        self.intelligent_branching = False
        # print("New solver:")
        # print(self.solution_to_string())

    def compute_solutions(self):
        # if len(self.last_updated) > 0:
        #     update_rows = list(set([int(lu[0]) for lu in self.last_updated]))
        #     update_cols = list(set([int(lu[1]) for lu in self.last_updated]))
        #     update_subsq = list(set([self.get_subsq(lu) for lu in self.last_updated]))
        #     for i in range(1, 10):  # row
        #         for j in range(1, 10):  # col
        #             if i in update_rows or \
        #                     j in update_cols or \
        #                     self.get_subsq(f"{i}{j}") in update_subsq:
        #                 self.update_cell_solutions(row=i, col=j)
        # else:
        #     for i in range(1, 10):  # row
        #         for j in range(1, 10):  # col
        #             self.update_cell_solutions(row=i, col=j)
        for a in range(1, 10):  # row
            for b in range(1, 10):  # col
                self.update_cell_solutions(row=a, col=b)

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
        self.last_updated = []
        for cell in self.possible_solutions.keys():
            if len(self.possible_solutions[cell]) == 1:
                row = int(cell[0])
                col = int(cell[1])
                self.solve_status[row - 1][col - 1] = self.possible_solutions[cell][0]
                self.possible_solutions[cell] = []
                self.last_updated.append(cell)
        self.check_solved()

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
        value_amounts = list(set([len(values) for values in self.possible_solutions.values()]))[1:]
        candidate_cells = [cell for cell in self.possible_solutions.keys()
                           if len(self.possible_solutions[cell]) == value_amounts[0]]

        # print("\n\n BRANCHING \n\n")
        # print(*self.solve_status, sep="\n")
        # print(f"{self.possible_solutions=}\n{candidate_cells=}")
        print(*self.solve_status, sep="\n")
        print(f"\n{self.possible_solutions=}\n{candidate_cells=}")
        if not self.intelligent_branching:
            return rd.choice(candidate_cells)
            # print(f"{candidate_cells[0]=}  {rd.choice(candidate_cells)=}\n")
            # return candidate_cells[0]
        else:
            pass  # TODO: find least ocurring values in candidate cells

    def get_subsq(self, cell):
        row = int(cell[0])
        col = int(cell[1])
        return (row - 1) // 3, (col - 1) // 3

    def solution_to_string(self):
        return "\n".join([" ".join(row) for row in self.solve_status])


def all_solved():
    global solvers
    for solver in solvers:
        if not solver.solved:
            return False
    return True


def remove_duplicates():
    global solvers
    for slv in reversed(range(0, len(solvers))):
        test_solver = solvers[slv]
        for j in reversed(range(0, slv)):
            if test_solver.solve_status == solvers[j].solve_status:
                solvers.pop(i)
                break


with open(INPUT_FILE) as sudoku_file:
    init_sudoku_solve_status = [line.split() for line in sudoku_file]

solvers = [SudokuSolver(init_sudoku_solve_status)]

debug_count = 0
while not all_solved():
    debug_count += 1
    print(f"BEFORE: {debug_count=} {len(solvers)=}")
    if len(solvers) > MAX_SUDOKUS:
        raise MemoryError("Amount of sudokus exceeded limit. Input sudoku is too vague.")
    for i in reversed(range(0, len(solvers))):
        if not solvers[i].solved:
            solvers[i].compute_solutions()
            if solvers[i].has_unique_values():
                solvers[i].assign_unique_values()
            elif solvers[i].is_impossible():
                solvers.pop(i)
            else:
                solvers.extend([SudokuSolver(status) for status in solvers[i].branch_solutions()])
                solvers.pop(i)
    print(f"AFTER: {debug_count=} {len(solvers)=}")
    remove_duplicates()

for i in range(len(solvers)):
    print(f"Solution n {i + 1}:")
    print(solvers[i].solution_to_string())
