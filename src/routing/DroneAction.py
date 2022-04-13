from src.simulation.Simulator import *
class DroneAction:
    def __init__(self, x: int, y: int, a: int, tau: float):
        if a == -1: assert x == y #(if charge than don't move)
        self.x = x
        self.y = y
        self.a = a
        self.tau = tau
        self.pred = None
        self.succ = None

    def __eq__(self, other):
        return isinstance(other, DroneAction) and self.x == other.x and self.y == other.y and self.a == other.a # and self.pred == other.pred and self.succ == other.succ

    def __str__(self):
        id_pred = None
        id_succ = None

        if self.pred is not None: id_pred = id(self.pred)
        if self.succ is not None: id_succ = id(self.succ)

        return f"'id': {id(self)}'x': {self.x}, 'y': {self.y}, 'a': {self.a}, 'tau': {self.tau}, 'pred': {id_pred}, 'succ':{id_succ}"

    def getDICT(self):
        return {
            'x': self.x,
            'y': self.y,
            'a': self.a,
            'tau': self.tau
        }

    def getTime(self, simulation):
        if self.a == -1:
            return SWAP_TIME
        else:
            return simulation.time(self.x, self.y)

