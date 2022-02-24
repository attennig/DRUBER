from src.simulation.Simulation import Simulation
from src.simulation.RandomGenerator import RandomGenerator
from src.routing.SchedulerMILP import SchedulerMILP
from src.config import *
import sys
GENERATE =  False
if __name__ == "__main__":
    ns, nu, nd = [int(arg) for arg in sys.argv[1:]]
    print(f"#############################################################\nStarting Simulation")
    S = Simulation(f"Seed{SIMULATION_SEED}_S{ns}U{nu}D{nd}")
    if GENERATE :
        G = RandomGenerator(S)
        try:
            G.generateRandomInstance(ns, nu, nd)
        except Exception as e:
            print(e)
        G.saveInstance()
    else:
        S.loadScenario()
    #map = S.getMap() # seve as map.png
    #map.savefig(f"{S.inFOLDER}/map.png") # img overlap
    S.computeSchedule()
    S.saveSolution()

    print(f"Closing Simulation")
    print("#############################################################")

    '''

    #generateRandomInstances()
    #print("hello")
    generateRandomInstance(5,3,2)

    assert len(sys.argv) == 2
    simulation_name = sys.argv[1]
    print(f"Simulation name: {simulation_name}")
    S = Simulation(simulation_name)
    #S.start()
    S.loadScenario()
    #'''

