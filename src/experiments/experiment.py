from src.simulation.Simulator import Simulator
from src.config import *
import os
from argparse import ArgumentParser

global mean_completion_time
global mean_execution_time
global mean_num_variables
global mean_num_constraints

def exec_simulation(size: int, seed: int, input_generation: bool, out_path: str, algorithm: str, method: str):
    #number_of_stations, seed, input_generation, out_path, algorithm
    print(f"#############################################################\nStarting Simulation")
    global mean_completion_time
    global mean_execution_time
    global mean_num_variables
    global mean_num_constraints
    S = Simulator(seed, size, out_path)
    if input_generation:
        S.generateRandomScenario()
    else:
        S.loadScenario()
    solution = None
    if algorithm != "NONE":
        if algorithm == "MILP": solution = S.run(algorithm, method)
        else: solution = S.run(algorithm)
        if solution is not None:
            S.saveSolution(solution)
            mean_completion_time += S.completion_time
            mean_execution_time += S.execution_time
            if algorithm == "MILP":
                mean_num_variables += S.num_variables
                mean_num_constraints += S.num_constraints


    print(f"Closing Simulation")
    print("#############################################################")
    return solution is not None


if __name__ == "__main__":

    parser = ArgumentParser(description=DESCRIPTION_STR)

    parser.add_argument("-n", dest='number_of_entities', action="store", type=int,
                        help="the number of entities in the simulation")

    parser.add_argument("-alg", dest='algorithm', action="store", type=str,
                        choices=ALGORITHMS, help="the optimization algorithm to use")

    #parser.add_argument("-method", dest='method', action="store", type=str, default=-1,
    #                    choices=list(MILP_METHODS.keys()), help="method used by MILP solver ")

    parser.add_argument("-g", dest='input_generation', action="store_true",
                         help="generte input")

    parser.add_argument("-out", dest='out_path', action="store", type=str,
                        help="path to output folder")


    parser.add_argument("-i_s", dest='initial_seed', action="store", type=int,
                        help="the initial seed (included) to use in the simualtion")
    parser.add_argument("-e_s", dest='end_seed', action="store", type=int,
                        help="the end seed (excluded) to use in the simualtion"
                             + "-notice that the simulations will run for seed in [+i_s, e_s)")


    args = parser.parse_args()


    number_of_entities = args.number_of_entities
    algorithm = args.algorithm
    method = ""
    if algorithm == "MILP": method = "concurrent" #args.method
    input_generation = args.input_generation
    out_path = args.out_path
    initial_seed = args.initial_seed
    end_seed = args.end_seed

    num_experiments = (end_seed-initial_seed)
    for seed in range(initial_seed, end_seed):
        feasible = exec_simulation(number_of_entities, seed, input_generation, out_path, algorithm, method)