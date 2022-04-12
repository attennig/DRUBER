from src.simulation.Simulator import Simulator

out_path = "./out/largeLOCAL" #"./out/example"

S = Simulator(1, 15, out_path)
S.loadScenario()
S.getMap().savefig(f"{S.outFOLDER}/map.png")
solution = S.run("LOCALSEARCH-LB")
S.saveSolution(solution)


