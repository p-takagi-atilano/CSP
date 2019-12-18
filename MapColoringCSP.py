# Paolo Takagi-Atilano, October 17, 2017

from ConstraintSatisfactionProblem import ConstraintSatisfactionProblem


class MapColoringCSP:
    def __init__(self, variables, domain, edges):   # graph_adjacency is list of string tuples
        self.variables = variables                  # given variables, aka places
        self.domain = domain                        # colors
        self.constraints = self.set_constraints(edges)
        self.CSP = ConstraintSatisfactionProblem(len(variables), len(domain), self.constraints)  # CSP

    # set constraints for CSP
    def set_constraints(self, edges):
        constraints = {}

        # two adjacent nodes may not be the same color
        not_same_color = set()
        for i in range(len(self.domain)):
            for j in range(len(self.domain)):
                if not self.domain[i] == self.domain[j]:
                    not_same_color.add((i, j))

        # iterate through each edge
        for i in range(len(edges)):

            # find index of one node in edge
            a = 0
            while self.variables[a] != edges[i][0]:
                a = a + 1

            # find index of other node in edge
            b = 0
            while self.variables[b] != edges[i][1]:
                b = b + 1

            # add set of constraints for edge to constraints dictionary
            constraints[(a, b)] = not_same_color
            constraints[(b, a)] = not_same_color

        return constraints

    # backtrack search
    def backtrack_search(self, mrv, lcv, inference):
        solution = {}
        self.CSP.backtrack_search(mrv, lcv, inference)

        #print(self.CSP.assignment)
        # sets number codes to corresponding variable name or color name
        for i in range(len(self.CSP.assignment)):

            solution[self.variables[i]] = self.domain[self.CSP.assignment[i]]

        return str(solution) + '\n        ' + str(self.CSP.fails) + " fails"
