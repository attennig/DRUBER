from src.simulation.Simulator import Simulator

out_path = "./out/large" #"./out/example"

S = Simulator(1, 20, out_path)
S.loadScenario()
S.getMap().savefig(f"{S.outFOLDER}/map.png")
solution = S.run("LOCALSEARCH")
S.saveSolution(solution)


