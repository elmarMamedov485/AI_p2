from solver import nQueens
import time

MAX = 1000
MIN = 10

def main():
    n = int(input("Provide n from [10, 1000]: "))

    if n <= MAX and n >= MIN:
        problem = nQueens(n)
        time_taken = None
        choice_file = input("Does input file exist? (y/n): ")

        if choice_file == "y":
            with open("input/nqueens.txt", "r") as file:
                contents = file.readlines()

            if len(contents) > n:
                 raise ValueError("Input length is greater than n")
            
            for line in contents:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" in line:
                    col, row = line.split("=")
                    col = int(col.strip())
                    row = int(row.strip())
                    problem.assignment[col] = row

        elif choice_file != "n" :
            raise ValueError("Wrong input")
        
        algorithm_choice = input("Choose algorithm (1. backtracking, 2. min-conflict): ")

        if int(algorithm_choice) == 1:
            start = time.time()
            print(problem.backtracking_search())
            end = time.time()
            time_taken = end - start
            print ("Time taken: ", time_taken, 'seconds')
        elif int(algorithm_choice) == 2:
            start = time.time()
            print(problem.min_confict(1000000))
            end = time.time()
            time_taken = end - start
            print ("Time taken: ", time_taken, 'seconds')
        else: 
            raise ValueError("Wrong input")

        print("Explored nodes: ", len(problem.explored_nodes))

        if int(algorithm_choice) == 1:
            with open(f"output/explored-{n}-Queens-backtracking.txt", "w") as file:
                file.write("Time taken: " + str(time_taken) + "s\n")
                for i in problem.explored_nodes:
                    i = str(i)
                    i += "\n"
                    file.write(i)
        elif int(algorithm_choice) == 2:
            with open(f"output/explored-{n}-Queens-min-conflict.txt", "w") as file:
                file.write("Time taken: " + str(time_taken) + "s\n")
                for i in problem.explored_nodes:
                    i = str(i)
                    i += "\n"
                    file.write(i)

    else:
        raise ValueError("Wrong input")  

if __name__ == "__main__":
    main() 
