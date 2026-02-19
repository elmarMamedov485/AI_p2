from solver import nQueens
import time

problem = nQueens(1000)
start = time.time()
print(problem.min_confict(100000000))
end = time.time()
print (end - start)