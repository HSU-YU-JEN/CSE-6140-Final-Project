# CSE-6140-Final-Project
Knapsack Problem

## How to execuete
To run the solver, navigate to the code directory and use the following command structure:

`python code/main.py -inst <filename> -alg [BnB|Approx|LS1|LS2] -time <cutoff in seconds> -seed <random seed>`

1， -inst <filename>: Specifies the dataset file path relative to the DATASET directory. For example, small_scale/small_1.\\

2. -alg [BnB|Approx|LS1|LS2]: Selects the algorithm to solve the Knapsack problem. Choose one from BnB, Approx, LS1, or LS2.\\
3. -time <cutoff in seconds>: Sets the maximum time in seconds that the algorithm is allowed to run.\\
4. -seed <random seed>: (Optional) Provides a seed for the random number generator. This is required for the local search algorithms (LS1 and LS2).\\

Examples:\\
`python code/main.py -inst small_scale/small_1 -alg LS1 -time 10 -seed 42`
