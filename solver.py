import random
from queue import Queue

class nQueens():

    def __init__(self, n):
        self.n = n  # Number of queens (and board size)
        self.assignment = {}  # Current variable → value assignments {column: row}
        self.domain = list(range(1, n+1))  # Possible row positions
        # Domains for each variable (column)
        self.domains = {i: self.domain[:] for i in range(1, n+1)}
        self.presearch = False  # Used to run AC-3 only once before search
        self.explored_nodes = []

    # Check if all variables have been assigned
    def complete_assignment(self):
        return len(self.assignment) == self.n
    
    # Least Constraining Value heuristic
    # Orders values based on how few conflicts they cause to neighbors
    def lcv(self, variable):
        val_conflict = {}

        for val in self.domains[variable]:
            conflict_count = 0

            for neighb in range(1, self.n + 1):
                if neighb != variable and neighb not in self.assignment:

                    d = abs(neighb - variable)

                    # Rows in neighbor that would be attacked
                    attacked_rows = {
                        val,          # same row
                        val + d,      # major diagonal
                        val - d       # minor diagonal
                    }

                    for r in attacked_rows:
                        if r in self.domains[neighb]:
                            conflict_count += 1

            val_conflict[val] = conflict_count

        #]Least constraining value first
        return sorted(val_conflict, key=val_conflict.get)
    

    # Minimum Remaining Values heuristic (MRV)
    # Select variable with smallest domain
    def select_var(self):
        min_domain_size = float('inf')
        var = None

        for i in range(1, self.n+1):
            if i not in self.assignment:
                if len(self.domains[i]) < min_domain_size:
                    min_domain_size = len(self.domains[i])
                    var = i
        
        return var
    
    # Check consistency of assigning val to var
    def assignment_consistent(self, var, val):
        for as_var, as_val in self.assignment.items():
            if not nQueens.constraints_check(var, as_var, val, as_val):
                return False
        return True
    
    # Forward Checking inference
    # After assigning variable, remove inconsistent values from neighbors
    def forward_checking(self, variable):
        domains = {var: val[:] for var, val in self.domains.items()}

        for i in range(1, self.n+1):
            if i != variable and i not in self.assignment:
                for vals in domains[i][:]:
                    # Remove values inconsistent with current assignment
                    if not nQueens.constraints_check(variable, i, self.domains[variable][0], vals):
                        domains[i].remove(vals)
                # If any domain becomes empty → failure
                if len(domains[i]) == 0:
                    return False, domains
        return True, domains

    # AC-3 algorithm after assigning a variable
    def AC_3(self, variable):
        q = Queue()
        domains = {var: val[:] for var, val in self.domains.items()}

        # Add arcs (neighbor → variable)
        for i in range(1, self.n+1):
            if i != variable and i not in self.assignment:
                q.put((i, variable))

        while not q.empty():
            x_i, x_j = q.get()

            # Revise domain of x_i
            if self.revise_of_ac3(x_i, x_j, domains):
                if len(domains[x_i]) == 0:
                    return False, domains
                
                # Add neighboring arcs back into queue
                for x_k in range(1, self.n+1):
                    if x_k != x_i and x_k not in self.assignment:
                        q.put((x_k, x_i))
        
        return True, domains
    
    # Full AC-3 preprocessing before search starts
    def AC_3_preseach(self):
        q = Queue()
        domains = {var: val[:] for var, val in self.domains.items()}

        # Add all arcs (i, j)
        for i in range(1, self.n+1):
            if i not in self.assignment:
                for j in range(1, self.n + 1):
                    if j not in self.assignment and i != j:
                        q.put((i, j))

        while not q.empty():
            x_i, x_j = q.get()

            if self.revise_of_ac3(x_i, x_j, domains):
                if len(domains[x_i]) == 0:
                    return False, domains
                
                for x_k in range(1, self.n+1):
                    if x_k != x_i and x_k not in self.assignment:
                        q.put((x_k, x_i))
        
        return True, domains

    # Revise step of AC-3
    # Remove values from x_i domain that have no supporting value in x_j domain
    def revise_of_ac3(self, x_i, x_j, domains):
        revised = False

        for x in domains[x_i][:]:
            satisfy = False
            for y in domains[x_j]:
                if nQueens.constraints_check(x_i, x_j, x, y):
                    satisfy = True
                    break
            if not satisfy:
                domains[x_i].remove(x)
                revised = True
        
        return revised
    
    # Entry point for backtracking search
    def backtracking_search(self):
        return self.backtrack()

    # Recursive backtracking algorithm
    def backtrack(self):
        if self.complete_assignment():
            return self.assignment
        
        
        # Run AC-3 once before search begins
        if not self.presearch:
            inferences, new_domains = self.AC_3_preseach()
            self.presearch = True
            if inferences:
                self.domains = new_domains
            else:
                return False, self.assignment

        variable = self.select_var()
        # Try values in LCV order
        for value in self.lcv(variable):
            self.explored_nodes.append(((variable, value), self.assignment.copy()))
            if self.assignment_consistent(variable, value):

                # Save state for backtracking
                old_assignment = self.assignment.copy()
                old_domains = {var: vals[:] for var, vals in self.domains.items()}

                self.assignment[variable] = value
                self.domains[variable] = [value]

                # Apply forward checking
                inferences, new_domains = self.forward_checking(variable)

                if inferences:
                    self.domains = {var: val[:] for var, val in new_domains.items()}
                    result = self.backtrack()

                    if result:
                        return result

                # Restore previous state (backtrack)
                self.domains = old_domains
                self.assignment = old_assignment
                self.explored_nodes.append("Backtrack ")


        return False                           
    
    # Min-Conflicts local search algorithm
    def min_confict(self, max_steps):
        conflicts_dict = {}

        # Initialize with random assignment
        for var in range(1, self.n + 1):
            self.assignment[var] = random.randrange(1, self.n + 1)
            conflicts_dict[var] = 0

        # Compute initial conflicts
        for i in range(1, self.n+1):
            for j in range(i+1, self.n+1):
                if not nQueens.constraints_check(i, j, self.assignment[i], self.assignment[j]):
                    conflicts_dict[i] += 1
                    conflicts_dict[j] += 1

        for _ in range(1, max_steps + 1):

            self.explored_nodes.append(self.assignment.copy())

            # If no conflicts → solution found
            if max(conflicts_dict.values()) == 0:
                return True, self.assignment
            
            # Pick random conflicted variable
            var = random.choice([var for var, val in conflicts_dict.items() if val != 0])

            min_c = float('inf')
            best_vals = []

            # Choose value minimizing conflicts
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
             
            # Remove old conflicts
            for i in range(1, self.n+1):
                if i != var and not nQueens.constraints_check(i, var, self.assignment[i], self.assignment[var]):
                    conflicts_dict[i] -= 1
                    conflicts_dict[var] -= 1

            # Assign best value
            self.assignment[var] = random.choice(best_vals)

            # Add new conflicts
            for i in range(1, self.n+1):
                if i != var and not nQueens.constraints_check(i, var, self.assignment[i], self.assignment[var]):
                    conflicts_dict[i] += 1
                    conflicts_dict[var] += 1

        return False, self.assignment 
        
    # Static constraint checker
    # Ensures:
    # 1) Not same row
    # 2) Not same diagonal
    @staticmethod
    def constraints_check(variable, neighb, val, val_neighb):
        if variable == neighb:
            return True
        if val == val_neighb:
            return False
        if abs(variable - neighb) == abs(val - val_neighb):
            return False
        return True
