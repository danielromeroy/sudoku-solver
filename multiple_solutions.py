import itertools as itt

INPUT_FILE = "./data/wikipedia_sudoku"
MAX_SUDOKUS = 10000


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
                            if ((i - 1) // 3) == ((k - 1) // 3) and \
                               ((j - 1) // 3) == ((l - 1) // 3) and \
                               self.solve_status[k - 1][l - 1] != "X":
                                nums_in_subsq.append(self.solve_status[k - 1][l - 1])

                    forbidden_nums = list(set(nums_in_row + nums_in_col + nums_in_subsq))

                    cell_possible_nums = [str(m) for m in range(1, 10) if str(m) not in forbidden_nums]

                    self.possible_nums[f"{i}{j}"] = cell_possible_nums

    def has_unique_solutions(self):
        has_unique = False
        for item in self.possible_nums.items():
            if len(item[1]) == 1:
                has_unique = True
                break
        return has_unique

    def assign_unique_values(self):
        for i in range(1, 10):  # row
            for j in range(1, 10):  # col
                if len(self.possible_nums[f"{i}{j}"]) == 1:
                    self.solve_status[i - 1][j - 1] = self.possible_nums[f"{i}{j}"][0]

        if "X" not in list(itt.chain(*self.solve_status)):
            self.solved = True

    def explode(self):
        # possible_solutions = []
        pass

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


with open(INPUT_FILE) as sudoku_file:
    init_sudoku_solve_status = [line.split() for line in sudoku_file]

solver = SudokuSolver(init_sudoku_solve_status)

while not solver.solved:
    solver.compute_possible_numbers()
    solver.assign_unique_values()

solver.print_string(1)
