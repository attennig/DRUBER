import gurobipy as gp
from gurobipy import GRB

class PathPlanner:

    def __init__(self):
        self.model = gp.Model("pathplanner")

    def findPath(self, mission, commitments):
        print("find path")
        # Graph
        edges = set()
        nodes = set()
        for c in commitments:
            edges.add((c.src.ID, c.dst.ID))
            nodes.add(c.src.ID)
            nodes.add(c.dst.ID)
        try:
            # Variables
            e = {}
            o_func_coeff = []
            for c in commitments:
                e[f"{c.src.ID}, {c.dst.ID}"] = self.model.addVar(vtype=GRB.BINARY, name=f"e_{c.src.ID}{c.dst.ID}")
                o_func_coeff.append((c.cost, e[f"{c.src.ID}, {c.dst.ID}"]))
            # Objective function
            print(e)
            o_func = gp.LinExpr(o_func_coeff)
            self.model.setObjective(o_func, GRB.MINIMIZE)

            # Contraints
            c1_coeff = []
            c2_coeff = []
            c3_coeff = []
            c4_coeff = []

            for c in commitments:
                print(f"{c.src.ID},{mission.src.ID}")
                # constraint: sum_i e[mission.src][i] = 1
                if c.src.ID == mission.src.ID:
                    c1_coeff.append((1.0, e[f"{c.src.ID}, {c.dst.ID}"]))
                # constraint: sum_i e[i][mission.src] = 0
                if c.dst.ID == mission.src.ID:
                    c2_coeff.append((1.0, e[f"{c.src.ID}, {c.dst.ID}"]))
                # constraint: sum_i e[mission.dst][i] = 0
                if c.src.ID == mission.dst.ID:
                    c3_coeff.append((1.0, e[f"{c.src.ID}, {c.dst.ID}"]))
                # constraint: sum_i e[i][mission.dst] = 1
                if c.dst.ID == mission.dst.ID:
                    c4_coeff.append((1.0, e[f"{c.src.ID}, {c.dst.ID}"]))

            # constraint 2.3b
            if len(c1_coeff) > 0:
                c1_func = gp.LinExpr(c1_coeff)
                self.model.addConstr(c1_func == 1, "c1")
            # constraint 2.3c
            if len(c2_coeff) > 0:
                c2_func = gp.LinExpr(c2_coeff)
                self.model.addConstr(c2_func == 0, "c2")
            # constraint 2.3d
            if len(c3_coeff) > 0:
                c3_func = gp.LinExpr(c3_coeff)
                self.model.addConstr(c3_func == 0, "c3")
            # constraint 2.3e
            if len(c4_coeff) > 0:
                c4_func = gp.LinExpr(c4_coeff)
                self.model.addConstr(c4_func == 1, "c4")

            # constraint 2.3f and 2.3g
            for j in nodes:
                if j == mission.src.ID or j == mission.dst.ID: continue
                coeff = []
                print(f"outedge dst endpoint of {j}: {set([edge[1] for edge in edges if edge[0] == j])}")
                for i in set([edge[1] for edge in edges if edge[0] == j]):
                    coeff.append((1.0, e[f"{j}, {i}"]))
                if len(coeff) > 0:
                    c6_func = gp.LinExpr(coeff)
                    self.model.addConstr(c6_func <= 1, f"c6-{j}")
                print(f"inedge src endpoint of {j}: {[edge[0] for edge in edges if edge[1] == j]}")
                for i in set([edge[0] for edge in edges if edge[1] == j]):
                    coeff.append((-1.0, e[f"{i}, {j}"]))
                if len(coeff) > 0:
                    c5_func = gp.LinExpr(coeff)
                    self.model.addConstr(c5_func == 0, f"c5-{j}")

            # constraint 2.3h
            self.model.addConstr(o_func <= mission.budget, "c7")

            # Save model in model.lp
            self.model.write("../data/model.lp")
            # Optimize model
            self.model.optimize()


            # Extract solution
            for v in self.model.getVars():
                print('%s %g' % (v.varName, v.x))

            print('Obj: %g' % self.model.objVal)

        except gp.GurobiError as err:
            print('Error code ' + str(err.errno) + ': ' + str(err))

        except AttributeError:
            print('Encountered an attribute error')
