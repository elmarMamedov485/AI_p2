from solver import nQueens
import time

problem = nQueens(1000)
start = time.time()
print(problem.backtracking_search())
end = time.time()
print (end - start)