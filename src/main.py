from Simulation import *
if __name__ == "__main__":
    DATAPATH = "../data/scenario0.json"
    S = Simulation(1)
    S.loadScenario(DATAPATH)
    S.showStatus()
    S.solve()
