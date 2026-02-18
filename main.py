from solver import nQueens
import time

problem = nQueens(99)
start = time.time()
print(problem.backtracking_search())
end = time.time()
print (end - start)