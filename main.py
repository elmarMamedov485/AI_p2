from solver import nQueens
import time

problem = nQueens(100)
start = time.time()
print(problem.backtracking_search())
end = time.time()
print (end - start)