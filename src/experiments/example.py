from src.simulation.Simulator import Simulator

out_path = "./out/example" #"./out/example"

S = Simulator(1, 18, out_path)
S.loadScenario()
#S.getMap().savefig(f"{S.outFOLDER}/map.png")
solution = S.run("LOCALSEARCH-HC")
S.saveSolution(solution)


