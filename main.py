from solver import nQueens
import time

MAX = 1000
MIN = 10

def main():
    n = int(input("Provide n from [10, 1000]:"))

    if n <= MAX and n >= MIN:
        problem = nQueens(n)
        choice_file = input("Does input file exist? (y/n): ")

        if choice_file == "y":
            with open("nqueens.txt", "r") as file:
                contents = file.readlines()

            if len(contents) > n:
                 raise ValueError("Input length is greater than n")
            
            for i, var in enumerate(contents):
                var = int(var)

                if var > 10 or var < 1:
                    raise ValueError("Incorrect file content")
                
                problem.assignment[i] = var
        elif choice_file != "n" :
            raise ValueError("Wrong input")
        
        algorithm_choice = input("Choose algorithm (1. backtracking, 2. min-conflict):")

        if int(algorithm_choice) == 1:
            start = time.time()
            print(problem.backtracking_search())
            end = time.time()
            print ("Time taken: ", end - start)
        elif int(algorithm_choice) == 2:
            start = time.time()
            print(problem.min_confict(1000000))
            end = time.time()
            print ("Time taken: ",end - start)
        else: 
            raise ValueError("Wrong input")

        print("Explored nodes: ", len(problem.explored_nodes))

        with open("explored.txt", "w") as file:
            for i in problem.explored_nodes:
                i = str(i)
                i += "\n"
                file.write(i)

    else:
        raise ValueError("Wrong input")  

if __name__ == "__main__":
    main() 
