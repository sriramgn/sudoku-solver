import itertools
import random

UNIVERSAL_SET = set(range(1,10))
n = None
problem1 = [
    [n, n, n, 6, n, n, 9, n, n],
    [n, n, n, n, n, 7, n, n, n],
    [n, 1, n, n, n, n, n, n, 3],
    [n, n, n, 2, n, n, n, n, n],
    [n, 5, n, n, 9, 6, n, n, n],
    [n, 4, 6, n, 5, 1, n, n, n],
    [n, n, n, 8, n, n, n, n, n],
    [n, n, n, 9, 7, 4, 3, n, 2],
    [n, n, 4, n, n, n, n, 6, 8],
]

def GetRowNumbers(row_no, problem):
    numbers = []
    for col_no in range(9):
        if problem[row_no][col_no] != None and type(problem[row_no][col_no]) == type(1):
            numbers.append(problem[row_no][col_no])
    return numbers

def GetColumnNumbers(col_no, problem):
    numbers = []
    for row_no in range(9):
        if problem[row_no][col_no] != None and type(problem[row_no][col_no]) == type(1):
            numbers.append(problem[row_no][col_no])
    return numbers

def GetDivisionalNumbers(row_no, col_no, problem):
    numbers = []
    div_row_start = int(row_no/3) * 3
    div_col_start = int(col_no/3) * 3
    for row in range(3):
        for col in range(3):
            if problem[div_row_start+row][div_col_start+col] != None and type(problem[div_row_start+row][div_col_start+col]) == type(1):
                numbers.append(problem[div_row_start+row][div_col_start+col])
    return numbers

def GetEmptyDivisionalCells(row_no, col_no, problem):
    div_cells = []
    row_cells = []
    col_cells = []
    div_row_start = int(row_no/3) * 3
    div_col_start = int(col_no/3) * 3
    for row in range(3):
        for col in range(3):
            if problem[div_row_start+row][div_col_start+col] == None:
                if not (row_no == (div_row_start+row) and col_no == (div_col_start+col)):
                    div_cells.append((div_row_start+row, div_col_start+col))

    for row in range(9):
        if row != row_no:
            if problem[row][col_no] == None:
                col_cells.append((row, col_no))

    for col in range(9):
        if col != col_no:
            if problem[row_no][col] == None:
                row_cells.append((row_no, col))

    return (div_cells, row_cells, col_cells)

def GetSolutionSet(row_no, col_no, problem):
    row_numbers = set(GetRowNumbers(row_no, problem))
    col_numbers = set(GetColumnNumbers(col_no, problem))
    div_numbers = set(GetDivisionalNumbers(row_no, col_no, problem))
    solution_set = UNIVERSAL_SET - row_numbers - col_numbers - div_numbers
    return solution_set

def GetCellCombinations(cell_list):
    combs = []
    for i in range(1,len(cell_list)+1):
        els = [list(x) for x in itertools.combinations(cell_list, i)]
        combs.append(els)
    return combs

def RemoveSolutionSet(cell_combos, problem, display=False):
    remove_from_solution_set = []
    for combosize in cell_combos:
        for combos in combosize:
            combo_solution_set = []
            for combo in combos:
               combo_solution_set.extend(list(GetSolutionSet(combo[0], combo[1], problem)))
            combo_solution_set = set(combo_solution_set)
            if len(combo_solution_set) == len(combos):
                remove_from_solution_set.extend(list(combo_solution_set))
    return set(remove_from_solution_set)

def DisplayProblem(problem):
    print (" -" + "---"*11 +"- ")
    i = 0
    for row in problem:
        str_row = list(map(lambda x : "x" if x==None else str(x), row))
        print ("| " + " | ".join(str_row) + " |")
        if i < 8:
            print ("| " + "---" * 11 + " |")
        else:
            print (" -" + "---"*11 +"- ")
        i+=1

def CheckSolved(problem):
    for row in problem:
        for col in row:
            if col == None:
                return False
    return True

def SolveIteratively(problem, assume=False):
    tot_solved = 0
    assumptions = []
    if CheckSolved(problem):
        return -1
    for i in range(9):
        for j in range(9):
            if problem[i][j] == None:
                solution_set = GetSolutionSet(i, j, problem)
                div_cells, row_cells, col_cells = GetEmptyDivisionalCells(i, j, problem)
                div_solution_set = []
                row_solution_set = []
                col_solution_set = []

                for div_cell in div_cells:
                    div_solution_set.extend(list(GetSolutionSet(div_cell[0], div_cell[1], problem)))
                for row_cell in row_cells:
                    row_solution_set.extend(list(GetSolutionSet(row_cell[0], row_cell[1], problem)))
                for col_cell in col_cells:
                    col_solution_set.extend(list(GetSolutionSet(col_cell[0], col_cell[1], problem)))

                row_cell_combos = GetCellCombinations(row_cells)
                col_cell_combos = GetCellCombinations(col_cells)
                div_cell_combos = GetCellCombinations(div_cells)

                remove_row_set = RemoveSolutionSet(row_cell_combos, problem)
                remove_col_set = RemoveSolutionSet(col_cell_combos, problem)
                remove_div_set = RemoveSolutionSet(div_cell_combos, problem, display=True if i==22 and j==5 else False)

                solution_set = solution_set - remove_row_set.union(remove_col_set, remove_div_set)
                if len(solution_set) == 1:
                    problem[i][j] = list(solution_set)[0]
                    tot_solved += 1

                if assume:
                    if len(solution_set) == 2:
                        assumptions.append(((i,j),list(solution_set)))
    if assume:
        if len(assumptions)>0:
            random_cell = random.randint(0,len(assumptions)-1)
            random_value = random.randint(0, len(assumptions[random_cell])-1)
            problem[assumptions[random_cell][0][0]][assumptions[random_cell][0][1]] = assumptions[random_cell][1][random_value]
            #problem[assumptions[-1][0][0]][assumptions[-1][0][1]] = assumptions[-1][1][0]
            tot_solved += 1

    return tot_solved


assume = False
number_of_assumptions = 0
for rounds in range(5000):
    solved = SolveIteratively(problem1, assume)
    if solved == 0:
        assume = True
        number_of_assumptions += 1
    elif solved == -1:
        print (f"Took {rounds} iterations to solve the puzzle. Number of assumptions = {number_of_assumptions}")
        break
    else:
        assume = False

DisplayProblem(problem1)
