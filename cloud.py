
from multiprocessing.pool import Pool


def test_solution(puzzle, solution):
    # indeks kolumn i wierszy
    ci = 0
    ri = 0

    # Tworzę kopię, by na niej pracować
    test_puzzle = [list(row) for row in puzzle]
    for sol_val in solution:
        # Znajdz puste pole 
        while test_puzzle[ri][ci] is not None:
            ci += 1
            if ci >= 9:
                ci = 0
                ri += 1

                if ri >= 9:
                    break

        if ri >= 9:
            break

        # ta wartośc w wierszu? zostaw
        if sol_val in test_puzzle[ri]:
            return False

        # ta wartośc w kolumnie? zostaw
        if sol_val in (x[ci] for x in test_puzzle):
            return False

        # ta wartośc w boxie? zostaw
        for box_ri in range((ri // 3) * 3, (ri // 3) * 3 + 3):
            for box_ci in range((ci // 3) * 3, (ci // 3) * 3 + 3):
                if test_puzzle[box_ri][box_ci] == sol_val:
                    return False

        # dobra wartosc, dopisz
        test_puzzle[ri][ci] = sol_val

    return True


def solve_puzzle(x, process_count=5):
    """Przyjmuje tablice od uzytkownika i zwraca rozwiazanie """
  

    ### Sprawdza dane od uzytkownika ###
    input_value_error = " Wejscie musi byc tablica 9x9! "
    if len(x) != 9:
        raise Exception(input_value_error)


    puzzle = [[None] * 9 for i in range(9)]
    
    var_count = 0
    for ri, row in enumerate(x):
        if len(row) != 9:
            raise Exception(input_value_error)

        for ci, element in enumerate(row):
            if element is None or element in ['x', '0']:
                var_count += 1
                continue

            puzzle[ri][ci] = int(element)

    if var_count == 0:
        return puzzle

    ### Brute force. ###
    possible_solutions = [[i+1] for i in range(9)]
    
    with Pool(process_count) as p:
        while True:
         
            for solution in possible_solutions:
                if len(solution) > var_count:
                    del solution

          
            if len(possible_solutions) == 0:
                raise Exception("Nie znaleziono rozwiazania :( ")

          
            test_solutions = possible_solutions
            test_success = p.starmap(test_solution, ((puzzle, solution) for solution in test_solutions))
            possible_solutions = []

            for i, success in list(enumerate(test_success)):
                
                if success:
            
                    if len(test_solutions[i]) == var_count:
                        for ri, row in enumerate(puzzle):
                            for ci, element in enumerate(row):
                                if element is None:
                                    puzzle[ri][ci] = test_solutions[i][0]
                                    del test_solutions[i][0]

                        return puzzle

                    
                    for j in range(9):
                        possible_solutions.append(test_solutions[i] + [j+1])


def str_to_puzzle(input_str):
    puzzle = [[None] * 9 for i in range(9)]

    for row_i, raw_row in enumerate(input_str.split('\n')):
        for column_i, value in enumerate([x for x in list(raw_row) if x not in [',', ' ']]):
            puzzle[row_i][column_i] = int(value) if value.lower() not in ['x', '0'] else None

    return puzzle


if __name__ == '__main__':
    print("Witam w rozwiązywaczu sudoku!")
    print("Podaj swoje cyfry (spacja miedzy numerami, uzywaj x jako puste pole): ")

    puzzle = ''

    # Gather input from the user.
    for row_i in range(9):
        raw_row = input("")
        puzzle += raw_row + '\n'

    puzzle = str_to_puzzle(puzzle[:-1])
    print(puzzle)

    print("\n W trakcie .....\n")

    solution = solve_puzzle(puzzle, process_count=8)

    print("Zrobione! Rozwiazanie niżej: ")

    for row_i in range(9):
        print(" ".join(map(str, solution[row_i])))