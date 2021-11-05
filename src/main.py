from Simulation import *
if __name__ == "__main__":
    N_TESTS = 7
    MODEL = 2

    for i in range(0,N_TESTS):
        print(f"Simulation n. {i}")
        datapath_in = f"../data/scenario{i}.json"
        datapath_out = f"../out/scenario{i}.out"
        S = Simulation(MODEL)
        S.loadScenario(datapath_in)
        S.showStatus()
        S.solve()
        S.saveSolution(datapath_out)
