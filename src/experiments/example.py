from src.simulation.Simulator import Simulator

out_path = "./out/smallC" #"./out/example"

S = Simulator(3, 6, out_path)
S.loadScenario()
S.getMap().savefig(f"{S.outFOLDER}/map.png")
solution = S.run("MILP", "concurrent")
S.saveSolution(solution)


