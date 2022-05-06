from src.simulation.Simulator import Simulator
from src.config import *
from argparse import ArgumentParser

parser = ArgumentParser(description=DESCRIPTION_STR)

parser.add_argument("-ns", dest='number_of_stations', action="store", type=int,
                    help="the number of supporting stations in the simulation")
parser.add_argument("-nd", dest='number_of_deliveries', action="store", type=int,
                    help="the number of drones in the simulation")
parser.add_argument("-nu", dest='number_of_drones', action="store", type=int,
                    help="the number of deliveries in the simulation")
parser.add_argument("-i_s", dest='initial_seed', action="store", type=int,
                    help="the initial seed (included) to use in the generation")
parser.add_argument("-e_s", dest='end_seed', action="store", type=int,
                    help="the end seed (excluded) to use in the generation"
                         + "- notice that the used seeds are [+i_s, e_s)")
parser.add_argument("-out", dest='out_path', action="store", type=str,
                        help="path to output folder")

parser.add_argument("-alg", dest='algorithm', action="store", type=str,
                        choices=ALGORITHMS, help="the optimization algorithm to use")
parser.add_argument("-method", dest='method', action="store", type=str,
                        help="the method for the optimization algorithm")

args = parser.parse_args()


for seed in range(args.initial_seed, args.end_seed):
    S = Simulator(seed, args.number_of_stations, args.number_of_deliveries, args.number_of_drones, args.out_path)
    S.loadScenario()
    solution = S.loadSolution(args.algorithm, args.method)

    if solution is not None:
        S.saveSolution(solution, args.algorithm, args.method, True)

