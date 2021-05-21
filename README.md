## Problem Statement
Use the **Mouth Brooding Fish (MBF) Algorithm** to solve the **Travelling Salesman Problem (TSP)**.

## The Travelling Salesman Problem
Given a set of cities, and the distance between each pair of connected cities, the problem is to find the shortest possible route which a salesman can traverse, visiting each city exactly once, and finally returning to the starting city.

## Mouth Brooding Fish Algorithm
Mouth Brooding Fish Algorithm (MBF) is also a search-based, nature inspired global optimization technique devised by observing the behaviour of an aquatic species called the mouthbrooders. It can be used to solve both discrete and continuous problems. When the mouthbrooder species lay their eggs, for the initial span of the offspring’s lifetime, the mother carries them in her mouth for protection from other dangerous species. After a while, the offsprings are released in the sea, but the mother stays nearby, and on any sign of danger, all the children run for protection in the mother’s mouth again. After certain time, when the mother is unable to fit all children in her mouth, certain weak offsprings are left behind in the water to face the danger by themselves.

The MBF algorithm is inspired by this behaviour of mouthbrooders. Initially we have a collection of possible solutions (population), which are affected by the mother’s source power, and other factors, while searching for the optimum value. They also undergo selection, mutation, and crossover, and moreover their movements are also guided by factors, which are inspired by the effect of nature on the mouthbrooders movements, and certain danger situations such as shark attacks. Certain movement decisions are also taken by the left-out offsprings who cannot seek shelter in the mother’s mouth. Fitness values are values assigned at each step to an individual of the population (chromosome), based on the optimization function value that the chromosome represents. Evolution, Mutation, and crossovers are decided either by probability sampling or by roulette-wheel selection. The algorithm is stopped when we reach a stopping criteria.

More details can be found from this [research paper](https://www.researchgate.net/publication/320104406_Tackling_global_optimization_problems_with_a_novel_algorithm_-_Mouth_Brooding_Fish_algorithm)

## Serial Algorithm
For the serial implementation of the Mouth Brooding Algorithm, we have generated a random initial path (solution) for all the member of the population (chromosomes). Then for each generation, we have updated the position(solution) of a chromosome by using swap operators as an alias for velocity, because velocity in literal terms makes little sense for our problem statement. Thus, we have used the chromosome’s previous velocity and changed the current position on it with a probability of SP (source power). We have attenuated the SP after each generation with the value SPdamp. We have also included swap operators by matching the chromosome’s current position with it’s personal best, with a probability of alpha (usually 1), whereas we have updated it after comparing with the global best solution with a probability of beta. After each generation we have randomly chosen 2 chromosomes, and performed one point crossover with 65% crossover of the fitter parent, and replaced the parents with the two offspring formed. The concept of left out cichlids, and nature force effect is irrelevant in the given problem statement since our search space includes all possible combination of the vertices. Hence the particle shall never go out of the search space.

## Complexity
For the given MBF algorithm, if we perform m iterations, over n population, calculating 3p swap operations in each generation, where p is the number of vertices, and 1 double crossover, the overall time complexity for the MBF algorithm is of the order O(mn(3p+1)), which is equivalent to O(mnp), which is same as that of the Genetic Algorithm. 

## Input Format
The algorithm inputs the number of vertices(n) from the user during runtime. **By default, the code is set to generate a complete weighted graph of n vertices**, and perform henceforth operations on it. However, if the user wants to input its own graph, another code has been commented at the bottom of the code, which can be used instead. The format of input in this case must be several lines each containing 3 values, the source vertex, the destination vertex, and the distance between them (weight of the edge). The file must be saved as input.txt in the same directory as that of the program.
- Ex.\
        1 2 5\
        1 3 4\
        2 3 7			---Indicates a complete graph with 3 vertices


## Output Format
The program outputs the final value of the global best solution, and its total path length. The Program can also output the intermediate states, as well as the shape of the graph, however those have been commented out, and can be used if necessary. The program also outputs the total execution time of the program.
 
## Test Cases
## The runtime for various values of the parameters is compared below


-   Population: 10\
    Number of iterations (Generations): 100\
    No. of vertices: 10\
    serial: 0.9783 seconds

-   Population: 10\
    Number of iterations (Generations): 1000\
    No. of vertices: 50\
    serial: 3.3097 seconds

-   Population: 20\
    Number of iterations (Generations): 1000\
    No. of vertices: 100\
    serial: 10.95 seconds

-   Population: 20\
    Number of iterations (Generations): 10000\
    No. of vertices: 100\
    serial: 12.404 seconds