from src.simulation.Simulator import *
class DroneAction:
    def __init__(self, x: Station, y: Station, a: int, tau: float):
        self.x = x
        self.y = y
        self.a = a
        self.tau = tau
        self.pred = None
        self.succ = None

    def __str__(self):
        return f"'x': {self.x}, 'y': {self.y}, 'a': {self.a}, 'tau': {self.tau}"

    def getDICT(self):
        return {
            'x': self.x,
            'y': self.y,
            'a': self.a,
            'tau': self.tau
        }
