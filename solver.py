from queue import Queue

class nQeens():

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
                if(neighb != variable):
                    for val_neighb in self.domains[neighb]:
                        if not nQeens.constraints_check(variable, neighb, val, val_neighb):
                            val_conflict[val] += 1

        return [val for val, _ in (sorted(val_conflict.items(), key = lambda item: item[1]))]

    def select_var(self):
        min = len(self.domains[1])
        var = 1

        for i in range(1, self.n+1):
            if i not in self.assignment:
                if len(self.domains[i]) < min:
                    min = len(self.domains[i])
                    var = i
        
        return var
    
    def assignment_constistent(self, var, val):
        for as_var, as_val in self.assignment:
            if not nQeens.constraints_check(var, as_var, val, as_val):
                return False
        return True
    
    def AC_3(self):
        q = Queue()

        for i in range(1, self.n+1):
            for j in range(i+1, self.n+1):
                q.put((i,j))

        while not q.empty():
            current_edge = q.get()
            x_i = current_edge[0]
            x_j = current_edge[1]

            if self.revise_of_ac3(x_i, x_j):
                if len(self.domains[x_i]) == 0:
                    return False
                
                for x_k in range(1, self.n+1):
                    if x_k != x_i:
                        q.put((x_k, x_i))
        
        return True

    def revise_of_ac3(self, x_i, x_j):
        revised = False

        for x in self.domains[x_i][:]:
            satisfy = False
            for y in self.domains[x_j]:
                if nQeens.constraints_check(x_i, x_j, x, y):
                    satisfy = True
            if not satisfy:
                self.domains[x_i].remove(x)
                revised = True
        
        return revised
    
    def backtracking_search(self):
        return self.backtrack()

    def backtrack(self):
        if self.complete_assignment():
            return self.assignment
        
        variable = self.select_var()

        for value in self.lcv(variable):
            if self.assignment_constistent(variable, value):
                self.assignment[variable] = value


        
    @staticmethod
    def constraints_check(variable, neighb, val, val_neighb):
        if(val == val_neighb):
            return False
        elif(abs(variable-neighb) == abs(val - val_neighb)):
            return False
        return True