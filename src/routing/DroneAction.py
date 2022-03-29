from src.simulation.Simulator import *
class DroneAction:
    def __init__(self, x: int, y: int, a: int, tau: float):
        assert a != -1 or x == y #(if charge than don't move)
        self.x = x
        self.y = y
        self.a = a
        self.tau = tau
        self.pred = None
        self.succ = None

    def __eq__(self, other):
        return isinstance(other, DroneAction) and self.x == other.x and self.y == other.y and self.a == other.a

    def __str__(self):
        return f"'x': {self.x}, 'y': {self.y}, 'a': {self.a}, 'tau': {self.tau}"

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

