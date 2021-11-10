from src.simulation.Simulation import Simulation


if __name__ == "__main__":
    max_TEST = 7
    min_TEST = 0


    for i in range(min_TEST,max_TEST):

        datapath_in = f"../data/scenario{i}.json"
        datapath_out = f"../out/scenario{i}.out"
        print(f"#############################################################\nStarting Simulation n. {i}")
        S = Simulation(i)
        S.loadScenario(datapath_in)
        S.showStatus()
        S.drawEnvironment()
        S.solve()
        print(f"Closing Simulation n. {i}")
        S.saveSolution(datapath_out)
        print("#############################################################")
