# Paolo Takagi-Atilano, October 17, 2017

from ConstraintSatisfactionProblem import ConstraintSatisfactionProblem


class CircuitBoardCSP:
    def __init__(self, length, height, pieces_list, square):
        self.length = length            # length of grid
        self.height = height            # height of grid
        self.pieces_list = pieces_list  # list of pieces

        self.constraints = self.set_constraints(square)     # constraints
        self.CSP = ConstraintSatisfactionProblem(len(pieces_list), self.length * self.height, self.constraints)  # CSP

    # set constraints for CSP
    def set_constraints(self, square):  # square format: (letter, length, height)
        constraints = {}

        pieces_location_list = []   # list of sets of all legal left-hand corners of each piece, for each piece
        for piece in self.pieces_list:
            # get set of all legal left-hand corners of each piece
            piece_location_set = set()
            for y in range(self.height):
                for x in range(self.length):
                    if x + piece[1] - 1 < self.length and y + piece[2] - 1 < self.height:
                        piece_location_set.add((piece, x, y))   # potential location of piece, and that piece
                        #print(piece_location_set)
            pieces_location_list.append(piece_location_set)

        for i in range(len(pieces_location_list)):
            for j in range(len(pieces_location_list)):
                if i != j:  # make sure we aren't comparing the same piece
                    common_location_list1 = set()    # set of all legal left-hand corners of pieces i and j
                    common_location_list2 = set()

                    for i_loc in pieces_location_list[i]:
                        for j_loc in pieces_location_list[j]:
                            #print("i_loc", i_loc, "j_loc:", j_loc)
                            #print(collision(i_loc, j_loc))
                            if not collision(i_loc, j_loc):
                                #print("adding:", (self.coord_to_int(i_loc[1], i_loc[2]),
                                # self.coord_to_int(j_loc[1], j_loc[2])  ))
                                common_location_list1.add( (self.coord_to_int(i_loc[1], i_loc[2]),
                                                           self.coord_to_int(j_loc[1], j_loc[2])  ))
                                common_location_list2.add( (self.coord_to_int(j_loc[1], j_loc[2]),
                                                           self.coord_to_int(i_loc[1], i_loc[2])  ))
                    constraints[(i, j)] = common_location_list1
                    constraints[(j, i)] = common_location_list2

        return constraints

    # given x and y values, return corresponding single int for some grid
    def coord_to_int(self, x, y):
        return y * self.length + x

    # given single int for some grid, return corresponding x and y values
    def int_to_coord(self, var):
        return var % self.length, int(var / self.length)

    # calls backtrack search object from CSP, and returns output plus some syntax
    def backtrack_search(self, mrv, lcv, inference):
        self.CSP.backtrack_search(mrv, lcv, inference)
        return self.solution_to_str(self.CSP.assignment) + "\n" + str(self.CSP.fails) + " fails" + "\n"

    # returns solution with nice syntax, rather than integers
    def solution_to_str(self, solution):
        sol_dict = {}
        sol_str = ""

        # iterate through pieces:
        for i in range(len(self.pieces_list)):
            # iterate through x and y values in each piece
            for x in range(self.pieces_list[i][1]):
                for y in range(self.pieces_list[i][2]):
                    # set that key to corresponding character symbol representing piece
                    pos = self.int_to_coord(solution[i])
                    ins = self.coord_to_int(x + pos[0], y + pos[1])
                    sol_dict[ins] = self.pieces_list[i][0]

        # setting blank spaces to periods
        for i in range(self.length * self.height):
            if i not in sol_dict.keys():
                sol_dict[i] = "."

        # turning dictionary into string
        for i in range(len(sol_dict.keys())):
            if i != 0 and i % self.length == 0:
                sol_str += "\n"
            sol_str += sol_dict[i]

        return sol_str


# resorts to brute force because some objects might not be rectangular
def collision(i_loc, j_loc):        # piece location: (piece, x, y), piece: (letter, length, height)
    for i_x in range(i_loc[1], i_loc[1] + i_loc[0][1]):  # iterate through x in first piece
        for i_y in range(i_loc[2], i_loc[2] + i_loc[0][2]):  # iterate through y in first piece
            for j_x in range(j_loc[1], j_loc[1] + j_loc[0][1]):  # iterate through x in second piece
                for j_y in range(j_loc[2], j_loc[2] + j_loc[0][2]):  # iterate through y in second piece
                    if i_x == j_x and i_y == j_y:
                        #print("collision", str(i_loc[0][0]), str(j_loc[0][0]), str(i_x), str(i_y))
                        return True
    # no collisions found
    return False
