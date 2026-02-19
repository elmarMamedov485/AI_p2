import random
from queue import Queue

class nQueens():

    def __init__(self, n):
        self.n = n
        self.assignment = {}
        self.domain = list(range(1, n+1))
        self.domains = {i: self.domain[:] for i in range(1, n+1)}
        self.presearch = False

    def complete_assignment(self):
        if len(self.assignment) < self.n:
            return False
        return True
    
    def lcv(self, variable):
        val_conflict = {}

        for i in self.domains[variable]:
            val_conflict[i] = 0
            
        for val in self.domains[variable]:
            for neighb in range(1, self.n+1):
                if neighb != variable and neighb not in self.assignment:
                    for val_neighb in self.domains[neighb]:
                        if not nQueens.constraints_check(variable, neighb, val, val_neighb):
                            val_conflict[val] += 1

        return [val for val, _ in (sorted(val_conflict.items(), key = lambda item: item[1]))]

    def select_var(self):
        min = float('inf')
        var = None

        for i in range(1, self.n+1):
            if i not in self.assignment:
                if len(self.domains[i]) < min:
                    min = len(self.domains[i])
                    var = i
        
        return var
    
    def assignment_consistent(self, var, val):
        for as_var, as_val in self.assignment.items():
            if not nQueens.constraints_check(var, as_var, val, as_val):
                return False
        return True
    
    def forward_checking(self, variable):
        domains = {var: val[:] for var, val in self.domains.items()}

        for i in range(1, self.n+1):
            if i != variable and i not in self.assignment:
                for vals in domains[i][:]:
                   
                    if not nQueens.constraints_check(variable, i, self.domains[variable][0], vals):
                        domains[i].remove(vals)
                if len(domains[i]) == 0:
                    return False, domains
        return True, domains

    def AC_3(self, variable):
        q = Queue()
        domains = {var: val[:] for var, val in self.domains.items()}

        for i in range(1, self.n+1):
            if i != variable and i not in self.assignment:
                q.put((i,variable))

        while not q.empty():
            current_edge = q.get()
            x_i = current_edge[0]
            x_j = current_edge[1]

            if self.revise_of_ac3(x_i, x_j, domains):
                if len(domains[x_i]) == 0:
                    return False, domains
                
                for x_k in range(1, self.n+1):
                    if x_k != x_i and x_k not in self.assignment:
                        q.put((x_k, x_i))
        
        return True, domains
    
    def AC_3_preseach(self):
        q = Queue()
        domains = {var: val[:] for var, val in self.domains.items()}

        for i in range(1, self.n+1):
            if i not in self.assignment:
                for j in range(1, self.n + 1):
                    if j not in self.assignment and i!=j:
                        q.put((i,j))

        while not q.empty():
            current_edge = q.get()
            x_i = current_edge[0]
            x_j = current_edge[1]

            if self.revise_of_ac3(x_i, x_j, domains):
                if len(domains[x_i]) == 0:
                    return False, domains
                
                for x_k in range(1, self.n+1):
                    if x_k != x_i and x_k not in self.assignment:
                        q.put((x_k, x_i))
        
        return True, domains

    def revise_of_ac3(self, x_i, x_j, domains):
        revised = False

        for x in domains[x_i][:]:
            satisfy = False
            for y in domains[x_j]:
                if nQueens.constraints_check(x_i, x_j, x, y):
                    satisfy = True
            if not satisfy:
                domains[x_i].remove(x)
                revised = True
        
        return revised
    
    def backtracking_search(self):
        return self.backtrack()

    def backtrack(self):
        if self.complete_assignment():
            return self.assignment
        
        if not self.presearch:
            inferences, new_domains = self.AC_3_preseach()
            self.presearch = True
            if inferences:
                self.domains = new_domains
            else: return False, self.assignment

        
        variable = self.select_var()

        for value in self.lcv(variable):
            if self.assignment_consistent(variable, value):
                old_assignment = self.assignment.copy()
                old_domains = {var: vals[:] for var, vals in self.domains.items()}
                self.assignment[variable] = value
                self.domains[variable] = [value]
                inferences, new_domains = self.forward_checking(variable)
                

                if inferences:
                    self.domains = {var: val[:] for var, val in new_domains.items()}

                    result = self.backtrack()

                    if result:         
                        return result 
                self.domains = old_domains
                self.assignment =  old_assignment
        return False                           

    def check_solution(self):
        for i in range(1, self.n+1):
            for j in range(i+1, self.n+1):
                if not self.constraints_check(i, j, self.assignment[i], self.assignment[j]):
                    return False
        return True
    
    def conflicted_variables(self):
        conflicted = set()
        for i in range(1, self.n+1):
            for j in range(i+1, self.n+1):
                if not nQueens.constraints_check(i, j, self.assignment[i], self.assignment[j]):
                    conflicted.add(i)
                    conflicted.add(j)
        return [var for var in conflicted]

    def min_confict(self, max_steps):
        for var in range(1, self.n + 1):
            self.assignment[var] =  random.randrange(1, self.n + 1)

        for i in range(1, max_steps + 1):
            if self.check_solution():
                return True, self.assignment
            
            var = random.choice(self.conflicted_variables())

            min_c = float('inf')
            best_vals = []

            for candidate_val in range(1, self.n + 1):
                cnt_conflicts = 0
                for assignment_var, assignment_val in self.assignment.items():
                    if var != assignment_var and not nQueens.constraints_check(var, assignment_var, candidate_val, assignment_val):
                        cnt_conflicts += 1
                if cnt_conflicts < min_c:
                    min_c = cnt_conflicts
                    best_vals = [candidate_val]
                elif cnt_conflicts == min_c:
                    best_vals.append(candidate_val)

            self.assignment[var] = random.choice(best_vals)

        return False, self.assignment 
        
    @staticmethod
    def constraints_check(variable, neighb, val, val_neighb):
        if(variable == neighb):
            return True
        if(val == val_neighb):
            return False
        if(abs(variable-neighb) == abs(val - val_neighb)):
            return False
        return True