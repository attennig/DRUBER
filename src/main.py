from src.simulation.Simulation import Simulation

if __name__ == "__main__":
    max_TEST = 9
    min_TEST = 0

    for i in range(min_TEST,max_TEST):
        print(f"#############################################################\nStarting Simulation n. {i}")
        S = Simulation(i)
        datapath_in = f"../data/scenario{i}.json"
        S.loadScenario(datapath_in)
        S.showStatus()
        S.solve()
        print(f"Closing Simulation n. {i}")
        datapath_out = f"../out/scenario{i}.out"
        S.saveSolution(datapath_out)
        S.drawSolution()
        print("#############################################################")
