from src.simulation.Simulation import Simulation

if __name__ == "__main__":
    #max_TEST = 9
    #min_TEST = 0
    FROM_FILE = False
    #for i in range(min_TEST,max_TEST):
    if FROM_FILE:
        i = 0
        print(f"#############################################################\nStarting Simulation n. {i}")
        S = Simulation(i)
        datapath_in = f"../data/scenario{i}.json"
        S.loadScenario(datapath_in)
        datapath_out = f"../out/scenario{i}.out"
    else:
        print(f"#############################################################\nStarting random Simulation")
        S = Simulation(100)
        N_stations, N_drones, N_deliveries, AoI_SIZE, H = 20,5,3,2,10
        #N_stations, N_drones, N_deliveries, AoI_SIZE, H = 20,5,3,2,20
        #N_stations, N_drones, N_deliveries, AoI_SIZE, H = 20,40,30,3,50
        S.generateRandomInstance(N_stations, N_drones, N_deliveries, AoI_SIZE, H)
        datapath_out = f"../out/random{[N_stations, N_drones, N_deliveries, AoI_SIZE, H]}.out"
    S.showStatus()
    S.solve()
    print(f"Closing Simulation")
    S.saveSolution(datapath_out)
    print("#############################################################")
