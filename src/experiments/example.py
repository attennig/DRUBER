from src.simulation.Simulator import Simulator

out_path = "./out/example"
S = Simulator(0, 9, out_path)
S.loadScenario()
#S.getMap().savefig(f"{S.outFOLDER}/map.png")
solution = S.run("LOCALSEARCH")
S.saveSolution(solution)


