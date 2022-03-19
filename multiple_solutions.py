import itertools as itt
import copy as c

INPUT_FILE = "data/wikipedia_sudoku"
MAX_SUDOKUS = 50000


class SudokuSolver:
    def __init__(self, init_status: list):
        self.solve_status = init_status
        self.possible_nums = {}
        self.possible_nums_amount = {}
        self.solved = False
        self.last_updated = []
        self.intelligent_branching = False
        self.digit_occurrences = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0,
            9: 0,
        }

    def compute_all_possible_numbers(self):
        print("Computing all solutions")
        self.possible_nums = {}
        for i in range(1, 10):  # row
            for j in range(1, 10):  # col
                self.possible_nums[f"{i}{j}"] = []
        for i in range(1, 10):  # row
            for j in range(1, 10):  # col
                self.update_cell(i, j)

    def compute_necessary_numbers(self):
        print("Computing only the necessary solutions")
        update_rows = []
        update_cols = []
        update_subsq = []
        for cell in self.last_updated:
            row = int(cell[0])
            if row not in update_rows:
                update_rows.append(row)
            col = int(cell[1])
            if col not in update_cols:
                update_cols.append(col)
            subsq = ((row - 1) // 3, (col - 1) // 3)
            if subsq not in update_subsq:
                update_subsq.append(subsq)

        for i in range(1, 10):  # row]
            for j in range(1, 10):  # col
                if i in update_rows or \
                   j in update_cols or \
                   ((i - 1) // 3, (j - 1) // 3) in update_subsq:
                    self.update_cell(i, j)

    def update_cell(self, row_n, col_n):
        if self.solve_status[row_n - 1][col_n - 1] == "X":
            row = self.solve_status[row_n - 1]
            nums_in_row = list(set(row))
            nums_in_row.remove("X")

            col = [self.solve_status[r - 1][col_n - 1] for r in range(1, 10)]
            nums_in_col = list(set(col))
            nums_in_col.remove("X")

            nums_in_subsq = []
            for k in range(1, 10):  # row
                for l in range(1, 10):  # col
                    # Check if current row and col are in the same subsquare
                    if ((row_n - 1) // 3) == ((k - 1) // 3) and \
                            ((col_n - 1) // 3) == ((l - 1) // 3) and \
                            self.solve_status[k - 1][l - 1] != "X":
                        nums_in_subsq.append(self.solve_status[k - 1][l - 1])

            forbidden_nums = list(set(nums_in_row + nums_in_col + nums_in_subsq))

            self.possible_nums[f"{row_n}{col_n}"] = [str(m) for m in range(1, 10) if str(m) not in forbidden_nums]

    def compute_solutions(self):
        if len(self.last_updated) > 0:
            self.compute_necessary_numbers()
        else:
            self.compute_all_possible_numbers()

    def has_unique_solutions(self):
        for item in self.possible_nums.items():
            if len(item[1]) == 1:
                return True
        return False

    def assign_unique_values(self):
        self.last_updated = []
        for i in range(1, 10):  # row
            for j in range(1, 10):  # col
                if len(self.possible_nums[f"{i}{j}"]) == 1:
                    self.solve_status[i - 1][j - 1] = self.possible_nums[f"{i}{j}"][0]
                    self.last_updated.append(f"{i}{j}")

        if "X" not in list(itt.chain(*self.solve_status)):
            self.solved = True

    def branch_solutions(self):
        branched_solutions = []
        for i in range(1, 10):  # row
            for j in range(1, 10):  # col
                self.possible_nums_amount[f"{i}{j}"] = len(self.possible_nums[f"{i}{j}"])

        least_solutions = tuple(set(self.possible_nums_amount.values()))[0]

        update_cells = []
        for i in range(1, 10):  # row
            for j in range(1, 10):  # col
                if self.possible_nums_amount[f"{i}{j}"] == least_solutions:
                    update_cells.append(f"{i}{j}")

        if not self.intelligent_branching:
            pass  # TODO: choose random cell and assign it
        else:
            pass  # TODO: implement search for least ocurring num
        return branched_solutions

    def least_vague_cells(self):
        pass  # TODO: find cells with the least amount of solutions

    def count_digits_in_possible_solutions(self):
        pass  # TODO: count numbers and assign digit_occurrences

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

debug_count = 0
while not all_solved():
    debug_count += 1
    print(f"{debug_count=} {len(solvers)=} (before operations)")
    if len(solvers) > MAX_SUDOKUS:
        raise MemoryError("Amount of sudokus exceeded limit. Input sudoku is too vague.")
    for i in reversed(range(0, len(solvers))):
        solver = solvers[i]
        if not solver.solved:
            solver.compute_solutions()
            if solver.has_unique_solutions():
                solver.assign_unique_values()
            else:
                solvers.pop(i)
                solvers.extend([SudokuSolver(status) for status in solver.branch_solutions()])
    print(f"{debug_count=} {len(solvers)=} (after operations)")
    remove_duplicates()

print(f"{debug_count=} {len(solvers)=} (end of operations)")

for i in range(len(solvers)):
    solvers[i].print_string(i + 1)
