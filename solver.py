from queue import Queue

class nQueens():

    def __init__(self, n):
        self.n = n
        self.assignment = {}
        self.domain = list(range(1, n+1))
        self.domains = {i: self.domain[:] for i in range(1, n+1)}

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
    
    def assignment_constistent(self, var, val):
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
                    if x_k != x_i:
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
        
        variable = self.select_var()

        for value in self.domains[variable]:
            if value in self.domains[variable] and self.assignment_constistent(variable, value):
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


        
    @staticmethod
    def constraints_check(variable, neighb, val, val_neighb):
        if(variable == neighb):
            return True
        if(val == val_neighb):
            return False
        if(abs(variable-neighb) == abs(val - val_neighb)):
            return False
        return True