from Simulation import *
if __name__ == "__main__":
    i = 3
    DATAPATH = f"../data/scenario{i}.json"
    MODEL = 2
    S = Simulation(MODEL)
    S.loadScenario(DATAPATH)
    S.showStatus()
    S.solve()
