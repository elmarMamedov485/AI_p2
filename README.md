## Description

The project solves n-Queens problem using CSP backtracking algorithm. Several heuristics are used: MRV, LCV. The project also implements AC-3 both for preprocessing and for usage during search. Additionally, forward checking is implemented. Despite all, the algorithm struggles to solve instances for n > 100. For this reason, min-conflicts alorithm is also provided. 

## How to use

Use the following command to clone the repository:

```
git clone https://github.com/elmarMamedov485/AI_p2
```

To run the code execute the following command:

```
python3 main.py
```

The input can be provide through console. It is possible to provide n, defining n-Queens problem. Otherwise user can provide partial assignment in the "output/nqueens.txt" in the following format "variable = value". Additionally, it is possible to choose either Backtrack or Min-Conflict algorithm.

Sample input 

```
python main.py                             
Provide n from [10, 1000]: 10
Does input file exist? (y/n): n
Choose algorithm (1. backtracking, 2. min-conflict): 1
```

Sample output

```
{1: 1, 2: 4, 3: 7, 4: 10, 8: 9, 5: 8, 10: 6, 6: 3, 7: 5, 9: 2}
Time taken:  0.0033979415893554688 seconds
Explored nodes:  10
```