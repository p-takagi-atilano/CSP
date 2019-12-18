# Paolo Takagi-Atilano, October 17, 2017

from ConstraintSatisfactionProblem import ConstraintSatisfactionProblem


class SudokuCSP:
    def __init__(self, given_numbers):

        self.given_numbers = given_numbers              # format: (value, x, y); 0,0 is the bottom left corner
        self.domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        self.given_dict = {}     # key is position, value is value
        # givens
        for given in self.given_numbers:
            self.given_dict[self.coord_to_int(given[1], given[2])] = given[0]

        self.constraints = self.set_constraints()
        self.CSP = ConstraintSatisfactionProblem(81, 10, self.constraints)      # hardcoded because sudoku

    def set_constraints(self):
        # first find the domain of every single value
        single_var_constraint = {}
        for x in range(10):
            for y in range(10):
                if self.coord_to_int(x, y) not in self.given_dict.keys():
                    local_can = self.local_can_values(x, y)
                    vertical_can = self.vertical_can_values(y)
                    horizontal_can = self.horizontal_can_values(x)

                    valid_vals = set()
                    for i in range(10):  # domain values that given x,y can be
                        if i in local_can and vertical_can and horizontal_can:
                            valid_vals.add(i)
                    single_var_constraint[self.coord_to_int(x, y)] = valid_vals

        # now create constraints
        constraints = {}
        for x_1 in range(10):
            for y_1 in range(10):
                for x_2 in range(10):
                    for y_2 in range(10):
                        if x_1 != x_2 and y_1 != y_2:   # check to make sure not the same square
                            common_location_list1 = set()
                            common_location_list2 = set()
                            if self.coord_to_int(x_1, y_1) in single_var_constraint.keys():
                                if self.coord_to_int(x_2, y_2) in single_var_constraint.keys():
                                    for val1 in single_var_constraint[self.coord_to_int(x_1, y_1)]:
                                        for val2 in single_var_constraint[self.coord_to_int(x_2, y_2)]:
                                            if self.no_influence(x_1, y_1, x_2, y_2):
                                                common_location_list1.add((val1, val2))
                                                common_location_list2.add((val2, val1))
                                            else:   # add all values except same values
                                                if val1 != val2:
                                                    common_location_list1.add((val1, val2))
                                                    common_location_list2.add((val2, val1))
                            if len(common_location_list1) > 0:
                                constraints[self.coord_to_int(x_1, y_1),
                                            self.coord_to_int(x_2, y_2)] = common_location_list1
                            if len(common_location_list2) > 0:
                                constraints[self.coord_to_int(x_2, y_2),
                                            self.coord_to_int(x_1, y_1)] = common_location_list2

        #print("constraints:",constraints)
        return constraints

    def no_influence(self, x_1, y_1, x_2, y_2):
        # see if on same row
        test1 = False
        test2 = False
        for x_loc in range(10):
            if x_loc == x_1:
                test1 = True
            if x_loc == x_2:
                test2 = True
        if test1 and test2:
            return False

        # see if on same column
        test1 = False
        test2 = False
        for y_loc in range(10):
            if y_loc == y_1:
                test1 = True
            if y_loc == y_2:
                test2 = True
        if test1 and test2:
            return False

        # test to see if in same 9-group:
        if 0 <= x_1 <= 2 and 0 <= y_1 <= 2 and 0 <= x_2 <= 2 and 0 <= y_2 <= 2:  # bottom left
            return False
        if 3 <= x_1 <= 5 and 0 <= y_1 <= 2 and 3 <= x_2 <= 5 and 0 <= y_2 <= 2:  # bottom middle
            return False
        if 6 <= x_1 <= 8 and 0 <= y_1 <= 2 and 6 <= x_2 <= 8 and 0 <= y_2 <= 2:  # bottom right
            return False
        if 0 <= x_1 <= 2 and 3 <= y_1 <= 5 and 0 <= x_2 <= 2 and 3 <= y_2 <= 5:  # middle left
            return False
        if 3 <= x_1 <= 5 and 3 <= y_1 <= 5 and 3 <= x_2 <= 5 and 3 <= y_2 <= 5:  # middle middle
            return False
        if 6 <= x_1 <= 8 and 3 <= y_1 <= 5 and 6 <= x_2 <= 8 and 3 <= y_2 <= 5:  # middle right
            return False
        if 0 <= x_1 <= 2 and 6 <= y_1 <= 8 and 0 <= x_2 <= 2 and 6 <= y_2 <= 8:  # top left
            return False
        if 3 <= x_1 <= 5 and 6 <= y_1 <= 8 and 3 <= x_2 <= 5 and 6 <= y_2 <= 8:  # top middle
            return False
        if 6 <= x_1 <= 8 and 6 <= y_1 <= 8 and 6 <= x_2 <= 8 and 6 <= y_2 <= 8:  # top right
            return False

        return True


    def vertical_can_values(self, y):
        good = set()
        bad = set()
        for x_loc in range(10):
            loc = self.coord_to_int(x_loc, y)
            if loc in self.given_dict.keys():
                bad.add(self.given_dict[loc])

        for i in range(len(self.domain)):
            if i not in bad:
                good.add(self.domain[i])
        return good

    def horizontal_can_values(self, x):
        good = set()
        bad = set()
        for y_loc in range(10):
            loc = self.coord_to_int(x, y_loc)
            if loc in self.given_dict.keys():
                bad.add(self.given_dict[loc])

        for i in range(len(self.domain)):
            if i not in bad:
                good.add(self.domain[i])
        return good

    # returns set of values that it cannot be, given x and y, based on given values:
    def local_can_values(self, x, y,):

        # find location within square of 9
        if x % 3 == 0:
            if y % 3 == 0:     # bottom left corner
                can_values = self.bottom_left(x, y)
            elif y % 3 == 1:   # bottom middle
                can_values = self.bottom_middle(x, y)
            else:              # bottom right
                can_values = self.bottom_right(x, y)
        elif x % 3 == 1:
            if y % 3 == 0:    # middle left corner
                can_values = self.middle_left(x, y)
            elif y % 3 == 1:  # middle middle
                can_values = self.middle_middle(x, y)
            else:             # middle right
                can_values = self.middle_right(x, y)
        else:
            if y % 3 == 0:    # top left corner
                can_values = self.top_left(x, y)
            elif y % 3 == 1:  # top middle
                can_values = self.top_middle(x, y)
            else:             # top right
                can_values = self.top_middle(x, y)

        return can_values

    def bottom_left(self, x, y):
        good = set()
        bad = set()
        for x_loc in range(x, x + 3):
            for y_loc in range(y, y + 3):
                if x_loc != x and y_loc != y:
                    loc = self.coord_to_int(x_loc, y_loc)
                    if loc in self.given_dict.keys():
                        bad.add(self.given_dict[loc])
        for i in range(len(self.domain)):
            if i not in bad:
                good.add(self.domain[i])
        return good

    def bottom_middle(self, x, y):
        good = set()
        bad = set()
        for x_loc in range(x - 1, x + 2):
            for y_loc in range(y, y + 3):
                if x_loc != x and y_loc != y:
                    loc = self.coord_to_int(x_loc, y_loc)
                    if loc in self.given_dict.keys():
                        bad.add(self.given_dict[loc])
        for i in range(len(self.domain)):
            if i not in bad:
                good.add(self.domain[i])
        return good

    def bottom_right(self, x, y):
        good = set()
        bad = set()
        for x_loc in range(x - 2, x + 1):
            for y_loc in range(y, y + 3):
                if x_loc != x and y_loc != y:
                    loc = self.coord_to_int(x_loc, y_loc)
                    if loc in self.given_dict.keys():
                        bad.add(self.given_dict[loc])
        for i in range(len(self.domain)):
            if i not in bad:
                good.add(self.domain[i])
        return good

    def middle_left(self, x, y):
        good = set()
        bad = set()
        for x_loc in range(x, x + 3):
            for y_loc in range(y - 1, y + 2):
                if x_loc != x and y_loc != y:
                    loc = self.coord_to_int(x_loc, y_loc)
                    if loc in self.given_dict.keys():
                        bad.add(self.given_dict[loc])
        for i in range(len(self.domain)):
            if i not in bad:
                good.add(self.domain[i])
        return good

    def middle_middle(self, x, y):
        good = set()
        bad = set()
        for x_loc in range(x - 1, x + 2):
            for y_loc in range(y - 1, y + 2):
                if x_loc != x and y_loc != y:
                    loc = self.coord_to_int(x_loc, y_loc)
                    if loc in self.given_dict.keys():
                        bad.add(self.given_dict[loc])
        for i in range(len(self.domain)):
            if i not in bad:
                good.add(self.domain[i])
        return good

    def middle_right(self, x, y):
        good = set()
        bad = set()
        for x_loc in range(x - 2, x + 1):
            for y_loc in range(y - 1, y + 2):
                if x_loc != x and y_loc != y:
                    loc = self.coord_to_int(x_loc, y_loc)
                    if loc in self.given_dict.keys():
                        bad.add(self.given_dict[loc])
        for i in range(len(self.domain)):
            if i not in bad:
                good.add(self.domain[i])
        return good

    def top_left(self, x, y):
        good = set()
        bad = set()
        for x_loc in range(x, x + 3):
            for y_loc in range(y - 2, y + 1):
                if x_loc != x and y_loc != y:
                    loc = self.coord_to_int(x_loc, y_loc)
                    if loc in self.given_dict.keys():
                        bad.add(self.given_dict[loc])
        for i in range(len(self.domain)):
            if i not in bad:
                good.add(self.domain[i])
        return good

    def top_middle(self, x, y):
        good = set()
        bad = set()
        for x_loc in range(x - 1, x + 2):
            for y_loc in range(y - 2, y + 1):
                if x_loc != x and y_loc != y:
                    loc = self.coord_to_int(x_loc, y_loc)
                    if loc in self.given_dict.keys():
                        bad.add(self.given_dict[loc])
        for i in range(len(self.domain)):
            if i not in bad:
                good.add(self.domain[i])
        return good

    def top_right(self, x, y):
        good = set()
        bad = set()
        for x_loc in range(x - 2, x + 1):
            for y_loc in range(y - 2, y + 1):
                if x_loc != x and y_loc != y:
                    loc = self.coord_to_int(x_loc, y_loc)
                    if loc in self.given_dict.keys():
                        bad.add(self.given_dict[loc])
        for i in range(len(self.domain)):
            if i not in bad:
                good.add(self.domain[i])
        return good

    # these can be hardcoded because it is sudoku
    def coord_to_int(self, x, y):
        return y * 10 + x

    def int_to_coord(self, var):
        return var % 10, int(var/10)

    # calls backtrack search object from CSP, and returns output plus some syntax
    def backtrack_search(self, mrv, lcv, inference):
        print("this happened")
        self.CSP.backtrack_search(mrv, lcv, inference)
        print(self.CSP.assignment)
