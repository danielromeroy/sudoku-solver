import itertools as itt
import copy as c

INPUT_FILE = "data/sudoku_256_solutions"
MAX_SUDOKUS = 50000


class SudokuSolver:
    def __init__(self, init_status: list):
        self.solve_status = init_status
        self.possible_nums = {}
        self.solved = False

    def compute_possible_numbers(self):
        self.possible_nums = {}
        for i in range(1, 10):
            for j in range(1, 10):
                self.possible_nums[f"{i}{j}"] = []

        for i in range(1, 10):  # row
            row = self.solve_status[i - 1]
            for j in range(1, 10):  # col
                if self.solve_status[i - 1][j - 1] == "X":
                    nums_in_row = list(set(row))
                    nums_in_row.remove("X")

                    col = [self.solve_status[r - 1][j - 1] for r in range(1, 10)]
                    nums_in_col = list(set(col))
                    nums_in_col.remove("X")

                    nums_in_subsq = []
                    for k in range(1, 10):  # row
                        for l in range(1, 10):  # col
                            # Check if current row and col are in the same subsquare
                            if ((i - 1) // 3) == ((k - 1) // 3) and \
                                    ((j - 1) // 3) == ((l - 1) // 3) and \
                                    self.solve_status[k - 1][l - 1] != "X":
                                nums_in_subsq.append(self.solve_status[k - 1][l - 1])

                    forbidden_nums = list(set(nums_in_row + nums_in_col + nums_in_subsq))

                    self.possible_nums[f"{i}{j}"] = [str(m) for m in range(1, 10) if str(m) not in forbidden_nums]

    def has_unique_solutions(self):
        for item in self.possible_nums.items():
            if len(item[1]) == 1:
                return True
        return False

    def assign_unique_values(self):
        for i in range(1, 10):  # row
            for j in range(1, 10):  # col
                if len(self.possible_nums[f"{i}{j}"]) == 1:
                    self.solve_status[i - 1][j - 1] = self.possible_nums[f"{i}{j}"][0]

        if "X" not in list(itt.chain(*self.solve_status)):
            self.solved = True

    def explode(self):
        possible_solutions = []
        for i in range(1, 10):  # row
            for j in range(1, 10):  # col
                if self.solve_status[i - 1][j - 1] == "X":
                    for num in self.possible_nums[f"{i}{j}"]:
                        new_solution = c.deepcopy(self.solve_status)
                        new_solution[i - 1][j - 1] = num
                        possible_solutions.append(new_solution)
        return possible_solutions

    def print_string(self, n):
        print(f"Solution number {n}:")

        sudoku_string = ""
        count = 0
        for num in list(itt.chain(*self.solve_status)):
            sudoku_string += f"{num} "
            count += 1
            if count == 9:
                count = 0
                sudoku_string += "\n"

        print(sudoku_string)


def all_solved():
    global solvers
    for solver in solvers:
        if not solver.solved:
            return False
    return True


def remove_duplicates():
    global solvers
    for i in reversed(range(0, len(solvers))):
        test_solver = solvers[i]
        for j in reversed(range(0, i)):
            if test_solver.solve_status == solvers[j].solve_status:
                solvers.pop(i)
                break


with open(INPUT_FILE) as sudoku_file:
    init_sudoku_solve_status = [line.split() for line in sudoku_file]

solvers = [SudokuSolver(init_sudoku_solve_status)]

# debug_count = 0
while not all_solved():
    # debug_count += 1
    # print(f"{debug_count=} {len(solvers)=}")
    if len(solvers) > MAX_SUDOKUS:
        raise MemoryError("Amount of sudokus exceeded limit. Input sudoku is too vague.")
    for i in reversed(range(0, len(solvers))):
        solver = solvers[i]
        if not solver.solved:
            solver.compute_possible_numbers()
            if solver.has_unique_solutions():
                solver.assign_unique_values()
            else:
                solvers.pop(i)
                solvers.extend([SudokuSolver(status) for status in solver.explode()])
    remove_duplicates()

for i in range(len(solvers)):
    solvers[i].print_string(i + 1)
