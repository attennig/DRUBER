from Simulation import *
if __name__ == "__main__":
    # DATAPATH = "../data/scenario0.json"
    DATAPATH = "../data/scenario1.json"

    # MODEL = 1
    MODEL = 2
    S = Simulation(MODEL)
    S.loadScenario(DATAPATH)
    S.showStatus()
    S.solve()
