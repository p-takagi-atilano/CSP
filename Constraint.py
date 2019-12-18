# Paolo Takagi-Atilano, October 17, 2017

class Constraint:
    def __init__(self, constraints):
        # this is a dictionary, where 2-int tuples map to sets of 2-int tuples
        # two variables map to all their corresponding constraints
        self.constraints = constraints

    # returns true if given partial assignment fulfills constraints, false otherwise
    def is_satisfied(self, partial_assignment):
        # partial assignment is a set of ints

        for i in range(len(partial_assignment)):
            for j in range(len(partial_assignment)):
                if partial_assignment[i] is not None and partial_assignment[j] is not None \
                        and i != j and (i,j) in self.constraints.keys():
                    #print("i: ", i)
                    #print("j: ", j)
                    if (partial_assignment[i], partial_assignment[j]) not in self.constraints[(i,j)]:
                        return False

        return True

    # returns number of values no longer accessible in domain for particular index given some partial assignment
    # for mrv heuristic
    def possible_count(self, partial_assignment, index):
        count = 0
        constrained_domains = set()
        for i in range(len(partial_assignment)):
            # if already set neighbor, then it is constraining given index:
            if partial_assignment[i] is not None and (i, index) in self.constraints.keys() and \
                            partial_assignment[i] not in constrained_domains:
                constrained_domains.add(partial_assignment[i])
                count += 1

        return count

    # given value, returns tuple: (value, number of values it rules out for all adjacent variables)
    # for assumed variable, aka insert_index
    # for lcv heuristic
    def constrain_count(self, partial_assignment, insert_index, domain_value):
        # copy the list, and add potential value
        potential_assignment = []
        for i in range(len(partial_assignment)):
            potential_assignment.append(partial_assignment[i])
        potential_assignment[insert_index] = domain_value

        count = 0

        # iterate through all unassigned neighbors of i
        for i in range(len(potential_assignment)):
            not_yet_constrained = True
            # check to see if unassigned neighbor
            if potential_assignment[i] is None and (insert_index, i) in self.constraints.keys():

                #for constraint in self.constraints[(insert_index, i)]:
                #    for

                # also iterate through other assigned neighbors of i, to make sure value is not already constrained
                for j in range(len(potential_assignment)):
                    if j != insert_index and potential_assignment[j] is not None and (j, i) in self.constraints.keys():
                        if potential_assignment[j] == domain_value:
                            not_yet_constrained = False

                if not_yet_constrained:
                    count += 1

        return domain_value, count

    # returns set of arcs of given var and unassigned neighbors of given partial assignment
    # for mac-3 inference
    def unassigned_neighbors(self, partial_assignment, var):
        neighbors = set()

        for i in range(len(partial_assignment)):
            if partial_assignment[i] is None and (var, i) in self.constraints.keys():
                neighbors.add((var, i))
                neighbors.add((i, var))

        return neighbors

    # returns constraints between two variables
    def get_constraints(self, var1, var2):
        if (var1, var2) in self.constraints.keys():
            return self.constraints[(var1, var2)]
        else:
            return None
