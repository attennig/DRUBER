from src.simulation.Simulation import Simulation
import sys

if __name__ == "__main__":

    print(f"#############################################################\nStarting random Simulation")
    print(len(sys.argv))
    N_stations, N_drones, N_deliveries, AoI_SIZE, H = sys.argv[1:]
    print(f"Parameters: |S| = {N_stations}, |U| = {N_drones}, |D| = {N_deliveries}, AoI size = {AoI_SIZE}, H = {H}")
    S = Simulation()
    #N_stations, N_drones, N_deliveries, AoI_SIZE, H = 20,5,3,2,10
    #N_stations, N_drones, N_deliveries, AoI_SIZE, H = 20,5,3,2,20
    #N_stations, N_drones, N_deliveries, AoI_SIZE, H = 20,40,30,3,50
    S.generateRandomInstance(int(N_stations), int(N_drones), int(N_deliveries), int(AoI_SIZE), int(H))
    datapath_out = f"./out/random{[N_stations, N_drones, N_deliveries, AoI_SIZE, H]}.out"
    S.showStatus()
    S.solve()
    print(f"Closing Simulation")
    S.saveSolution(datapath_out)
    print("#############################################################")
