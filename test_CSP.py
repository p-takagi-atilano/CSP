# Paolo Takagi-Atilano, October 17, 2017

from MapColoringCSP import MapColoringCSP
from CircuitBoardCSP import CircuitBoardCSP
from SudokuCSP import SudokuCSP

# map coloring csp
variables = ["NT", "T", "V", "WA", "NSW", "Q", "SA"]
colors = ["r", "g", "b"]
edges = [("WA", "NT"), ("NT", "Q"), ("Q", "NSW"), ("NSW", "V"),
         ("WA", "SA"), ("NT", "SA"), ("Q", "SA"), ("NSW", "SA"), ("V", "SA")]

australia = MapColoringCSP(variables, colors, edges)
print("australia MapColoringCSP:")
print("    naive backtrack:")
print("       ", australia.backtrack_search(False, False, False))

print("    naive backtrack w/ inference:")
print("       ", australia.backtrack_search(False, False, True))

print("    mrv heuristic only:")
print("       ", australia.backtrack_search(False, False, False))

print("    mrv heuristic only w/ inference:")
print("       ", australia.backtrack_search(False, False, True))

print("    lcv heuristic only:")
print("       ", australia.backtrack_search(False, True, False))

print("    lcv heuristic only w/ inference:")
print("       ", australia.backtrack_search(False, True, True))

print("    both heuristics only:")
print("       ", australia.backtrack_search(True, True, False))
print("    both heuristics only w/ inference:")
print("       ", australia.backtrack_search(True, True, True))

# circuit board CSP
length = 10
height = 3
pieces_list = [('a', 3, 2), ('b', 5, 2), ('c', 2, 3), ('e', 7, 1)]  # square format: (letter, length, height)

circuit = CircuitBoardCSP(length, height, pieces_list, True)
print("\ncircuit CircuitBoardCSP:")

print("naive backtrack:")
print(circuit.backtrack_search(False, False, False))
print("naive backtrack w/ inference:")
print(circuit.backtrack_search(False, False, True))
print("mrv heuristic only:")
print(circuit.backtrack_search(True, False, False))
print("mrv heuristic only w/ inference:")
print(circuit.backtrack_search(True, False, True))
print("lcv heuristic only:")
print(circuit.backtrack_search(False, True, False))
print("lcv heuristic only w/ inference:")
print(circuit.backtrack_search(False, True, True))
print("both heuristics only:")
print(circuit.backtrack_search(True, True, False))
print("both heuristics only w/ inference:")
print(circuit.backtrack_search(True, True, True))

# sudoku CSP
# format: (value, x, y); 0,0 is the bottom left corner
given_numbers = [(9, 0, 0), (5, 1, 1), (3, 1, 2), (7, 2, 0), (6, 2, 1),
              (1, 4, 1), (4, 5, 2),
              (4, 6, 0), (5, 7, 0), (1, 8, 0), (9, 6, 1), (3, 8, 1), (6, 6, 2), (7, 7, 2),
              (5, 0, 5), (9, 1, 3), (8, 2, 5),
              (4, 3, 3), (8, 4, 3), (6, 4, 4), (9, 4, 5), (2, 5, 5),
              (2, 6, 3), (4, 7, 5), (7, 8, 3),
              (3, 0, 7), (1, 0, 8), (6, 1, 8), (5, 2, 8), (2, 2, 7), (9, 2, 6), (8, 1, 6),
              (6, 3, 6), (7, 4, 7),
              (7, 6, 8), (1, 6, 7), (6, 7, 7), (3, 7, 6), (8, 8, 8)]
sudoku = SudokuCSP(given_numbers)
#for key in sudoku.constraints.keys():
    #print("key", key)
    #print("constraints", sudoku.constraints[key])
#sudoku.backtrack_search(False, False, False)
