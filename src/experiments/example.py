from src.simulation.Simulator import Simulator

out_path = "./out" #"./out/example"

S = Simulator(1, 20, 5, 2, out_path)
S.loadScenario()
sol = S.loadSolution("LOCALSEARCH", "BFSOPT")
print(sol)
S.saveSolution(sol, "LOCALSEARCH", "BFSOPT", True)



