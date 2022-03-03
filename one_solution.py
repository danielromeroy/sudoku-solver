import itertools as itt

INPUT_FILE = "./data/wikipedia_sudoku"

with open(INPUT_FILE) as sudoku_file:
    sudoku_solve_status = [line.split() for line in sudoku_file]


def compute_possible_numbers(sudo_status):
    all_possible_nums = {}
    for i in range(1, 10):
        for j in range(1, 10):
            all_possible_nums[f"{i}{j}"] = []

    for i in range(1, 10):  # row
        row = sudo_status[i - 1]
        for j in range(1, 10):  # col
            if sudo_status[i - 1][j - 1] == "X":
                nums_in_row = list(set(row))
                nums_in_row.remove("X")

                col = [sudo_status[r - 1][j - 1] for r in range(1, 10)]
                nums_in_col = list(set(col))
                nums_in_col.remove("X")

                nums_in_subsq = []
                for k in range(1, 10):  # row
                    for l in range(1, 10):  # col
                        # Check if current row and col are in the same subsquare
                        if ((i - 1) // 3) == ((k - 1) // 3) and \
                           ((j - 1) // 3) == ((l - 1) // 3) and \
                           sudo_status[k - 1][l - 1] != "X":
                            nums_in_subsq.append(sudo_status[k - 1][l - 1])

                forbidden_nums = list(set(nums_in_row + nums_in_col + nums_in_subsq))

                cell_possible_nums = [str(m) for m in range(1, 10) if str(m) not in forbidden_nums]

                all_possible_nums[f"{i}{j}"] = cell_possible_nums
    return all_possible_nums


solved = False
# debug_count = 0
while not solved:
    # debug_count += 1
    # print(f"{debug_count=}")
    possible_nums = compute_possible_numbers(sudoku_solve_status)
    has_unique = False
    for item in possible_nums.items():
        if len(item[1]) == 1:
            has_unique = True
            break

    if not has_unique:
        raise ValueError("Sudoku has various solutions.")

    for i in range(1, 10):  # row
        for j in range(1, 10):  # col
            if len(possible_nums[f"{i}{j}"]) == 1:
                sudoku_solve_status[i - 1][j - 1] = possible_nums[f"{i}{j}"][0]

    if "X" not in list(itt.chain(*sudoku_solve_status)):
        solved = True


sudoku_string = ""
count = 0
for num in list(itt.chain(*sudoku_solve_status)):
    sudoku_string += f"{num} "
    count += 1
    if count == 9:
        count = 0
        sudoku_string += "\n"

print(sudoku_string)
