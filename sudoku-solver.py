import itertools
import random

# ANSI escape codes for colors
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'

# ANSI escape codes for background colors
BG_BLACK = '\033[40m'
BG_RED = '\033[41m'
BG_GREEN = '\033[42m'
BG_YELLOW = '\033[43m'
BG_BLUE = '\033[44m'
BG_MAGENTA = '\033[45m'
BG_CYAN = '\033[46m'
BG_WHITE = '\033[47m'

# ANSI escape code for resetting colors
RESET = '\033[0m'

UNIVERSAL_SET = set(range(1,10))

n = None

hardest_problem = [
    [8, n, n, n, n, n, n, n, n],
    [n, n, 3, 6, n, n, n, n, n],
    [n, 7, n, n, 9, n, 2, n, n],
    [n, 5, n, n, n, 7, n, n, n],
    [n, n, n, n, 4, 5, 7, n, n],
    [n, n, n, 1, n, n, n, 3, n],
    [n, n, 1, n, n, n, n, 6, 8],
    [n, n, 8, 5, n, n, n, 1, n],
    [n, 9, n, n, n, n, 4, n, n],
]

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

DEAD_ASSUMPTIONS = []
ASSUMPTION_CHAIN = ""
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

def print_color(text, text_color, background_color):
    print(background_color + text_color + text + RESET)

def DisplayProblem(problem):
    print (BG_YELLOW+BLACK+" "*16+" SOLUTION"+" "*16+RESET)
    for i in range(9):
        row_text = ""
        row2_text = ""
        row0_text = ""
        row_text += (BG_YELLOW+BLACK+"  "+RESET)
        row2_text += (BG_YELLOW+BLACK+"  "+RESET)
        row0_text += (BG_YELLOW+BLACK+"  "+RESET)
        for j in range(9):
            div_row = int(i/3)
            div_col = int(j/3)
            color = BLACK
            bg = BG_WHITE
            if (div_row+div_col)%2 == 1:
                color = WHITE
                bg = BG_BLACK
            row_text += bg + color
            if i == 2 or i == 5 or i == 8:
                row2_text += BG_WHITE + BLACK
                row0_text += BG_WHITE + BLACK
            else:
                row2_text += bg + color
                row0_text += bg + color
            if i == 0:
                row0_text += BG_WHITE + BLACK
            if j == 0:
                row_text += BG_WHITE + BLACK
                row2_text += BG_WHITE + BLACK
                row_text += "|"
                row2_text += "+"
                row0_text += "+"
                row_text += bg + color
                if i != 5:
                    row2_text += bg + color
            row_text += " " +BG_RED+WHITE+"x"+RESET+bg+color if problem[i][j]==None else " "+str(problem[i][j])
            row2_text += " -"
            row0_text += " -"
            if j == 5 or j == 2 or j == 8:
                row_text += " " + BG_WHITE + BLACK + "|"
                row2_text += " " + BG_WHITE + BLACK + "+"
                row0_text += " " + BG_WHITE + BLACK + "+"
            else:
                row_text += " |"
                row2_text += " +"
                row0_text += " +"
            row_text += RESET
            row2_text += RESET
            row0_text += RESET
        row_text += (BG_YELLOW+BLACK+"  "+RESET)
        row2_text += (BG_YELLOW+BLACK+"  "+RESET)
        row0_text += (BG_YELLOW+BLACK+"  "+RESET)
        if i==0:
            print (row0_text)
        print (row_text)
        print (row2_text)
    print (BG_YELLOW+BLACK+" "*41+RESET)

def CheckSolved(problem):
    for row in problem:
        for col in row:
            if col == None:
                return False
    return True

def SolveIteratively(problem, assume=False):
    global ASSUMPTION_CHAIN
    tot_solved = 0
    assumptions = []
    if CheckSolved(problem):
        return -1
    for i in range(9):
        for j in range(9):
            if problem[i][j] == None:
                solution_set = GetSolutionSet(i, j, problem)
                div_cells, row_cells, col_cells = GetEmptyDivisionalCells(i, j, problem)

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
            assumption_key = f"{assumptions[random_cell][0]}-{assumptions[random_cell][1][random_value]};"
            if assumption_key in DEAD_ASSUMPTIONS:
                return 0
            problem[assumptions[random_cell][0][0]][assumptions[random_cell][0][1]] = assumptions[random_cell][1][random_value]
            ASSUMPTION_CHAIN += assumption_key
            #problem[assumptions[0][0][0]][assumptions[0][0][1]] = assumptions[0][1][0]
            tot_solved += 1
        else:
            return -2

    return tot_solved


def SolveProblem(problem):
    global ASSUMPTION_CHAIN
    assume = False
    number_of_assumptions = 0
    ASSUMPTION_CHAIN = ""
    for rounds in range(162):
        solved = SolveIteratively(problem, assume)
        if solved == 0:
            assume = True
            number_of_assumptions += 1
        elif solved == -1:
            #print (f"Took {rounds} iterations to solve the puzzle. Number of assumptions = {number_of_assumptions}")
            return True
        elif solved == -2:
            #print (f"Took {rounds} iterations. Could not solve this problem.")
            if ASSUMPTION_CHAIN != "":
                DEAD_ASSUMPTIONS.append(ASSUMPTION_CHAIN)
            return False
        else:
            assume = False
    return False

def AttemptSolveProblem(problem):
    import json
    for attempt in range(1000):
        nproblem = json.loads(json.dumps(problem))
        if SolveProblem(nproblem):
            DisplayProblem(nproblem)
            break

AttemptSolveProblem(hardest_problem)
