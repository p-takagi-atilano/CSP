# Paolo Takagi-Atilano, October 17, 2017

from Constraint import Constraint


class ConstraintSatisfactionProblem:
    def __init__(self, assignment_length, domain_length, constraints):
        self.fails = 0

        self.assignment = []                        # array of ints
        self.assignment_length = assignment_length  # int corresponding to number of variables
        # set to none and of proper size
        for i in range(assignment_length):
            self.assignment.append(None)

        self.domain_length = domain_length          # int corresponding to number of entries in domain

        self.constraints = Constraint(constraints)

    # runs setup, then starts recursive backtrack search
    def backtrack_search(self, mrv, lcv, infer):
        # reset some necessary instance variables
        self.fails = 0
        for i in range(self.assignment_length):
            self.assignment[i] = None

        # calls the recursive backtrack search
        self.backtrack_search_helper(mrv, lcv, infer, {})

    # recursive backtrack search
    def backtrack_search_helper(self, mrv, lcv, infer, inconsistencies):

        print("Decided:", self.assignment)

        # base case: assignment is complete and valid
        if self.is_complete() and self.constraints.is_satisfied(self.assignment):
            return self.assignment

        # minimum remaining values heuristic
        if mrv:
            var = self.mrv_heuristic()
        else:
            var = self.no_variable_heuristic()

        # least constraining value heuristic
        if lcv:
            domain_list = self.lcv_heuristic(var)
        else:
            domain_list = []
            for i in range(self.domain_length):
                domain_list.append(i)

        if infer:   # find infer values
            if var in inconsistencies.keys():
                for inconsistency in inconsistencies[var]:
                    if inconsistency in domain_list:
                        domain_list.remove(inconsistency)   # don't consider inconsistencies

        #print("domain list: ", domain_list)
        for val in domain_list:

            self.assignment[var] = val
            print("trying val; ", val, ";", self.assignment, ";", self.constraints.is_satisfied(self.assignment))

            if self.constraints.is_satisfied(self.assignment):
                if infer:
                    inconsistencies = self.mac_infer(var)   # find inconsistencies from inference
                    #print(inconsistencies)
                    if inconsistencies is not None:
                        result = self.backtrack_search_helper(mrv, lcv, infer, inconsistencies)
                    else:
                        return None

                else:
                    result = self.backtrack_search_helper(mrv, lcv, infer, inconsistencies)

                if result is not None:  # potential value found, use it for previous recursive iteration
                    return result

            else:   # increment fails
                self.fails += 1

            # backtracking
            self.assignment[var] = None

        # no solution, return None
        return None

    # checks to see if assignment is complete
    def is_complete(self):
        for i in range(self.assignment_length):
            if self.assignment[i] is None:
                return False
        return True

    # returns next variable
    def no_variable_heuristic(self):
        for i in range(self.assignment_length):
            if self.assignment[i] is None:
                return i
                #return range(i, self.assignment_length)
        return 0

    # returns variable based on minimum remaining values
    def mrv_heuristic(self):

        min_remaining = (None, float('-inf'))
        # iterate through unassigned variables
        for i in range(self.assignment_length):
            if self.assignment[i] is None:
                temp = self.constraints.possible_count(self.assignment, i)
                # if more constraining than previous most constraining, it is the new most constraint
                if temp > min_remaining[1]:
                    min_remaining = (i, temp)

        return min_remaining[0]

    # returns values based on least constrained value
    def lcv_heuristic(self, var):

        tuple_list = []
        domain_list = []

        # iterate through each possible value
        for i in range(self.domain_length):
            lc_val = self.constraints.constrain_count(self.assignment, var, i)

            #print("*", lc_val)

            # find correct index to insert
            j = 0
            index = 0
            while j < len(tuple_list):
                if tuple_list[j][1] < lc_val[1]:
                    index += 1
                j += 1
            tuple_list.insert(index, lc_val)

        for i in range(len(tuple_list)):
            domain_list.append(tuple_list[i][0])

        #print("domain list:",domain_list, "\n")
        return domain_list

    # mac-3 inference
    def mac_infer(self, var):
        # dictionary mapping unassigned var ints to set of values that they cannot be:
        inconsistencies = {}
        queue = []

        # add all arcs with with one unassinged variables and given variable in them
        for initial in self.constraints.unassigned_neighbors(self.assignment, var):
            queue.append(initial)

        while queue:    # iterate through arcs
            arc = queue.pop()
            temp = self.mac_revise(arc, inconsistencies)

            # occurs when no possible value for some variable, means this tree is bad
            if temp is None:
                return None

            # add inconsistencies if found
            inconsistencies[arc[0]] = temp

        #print("inconsistencies:", inconsistencies)
        return inconsistencies

    # determines if arc is an inconsistency
    def mac_revise(self, arc, inconsistencies):
        # set of all values var1 and var2 cannot be
        revised = set()
        if arc[0] in inconsistencies.keys():
            revised = inconsistencies[arc[0]]

        constraints = self.constraints.get_constraints(arc[0], arc[1])
        #print("constraints:",constraints)
        if constraints is None:
            return None

        # iterate through assignment, looking for inconsistencies
        for x in range(self.domain_length):
            cannot = 0
            for y in range(self.domain_length):
                if (x, y) not in constraints:
                    cannot += 1
            if cannot == self.domain_length:
                revised.add(x)

        # no possible values, bad decision in past
        if len(revised) == self.domain_length:
            return None

        return revised
