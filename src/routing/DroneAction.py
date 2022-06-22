from src.simulation.Simulator import *
class DroneAction:
    def __init__(self, type: str, x: int, y: int, d: int, p: int, tau: float):
        self.type = type
        self.x = x
        self.y = y
        self.d = d
        self.p = p
        self.tau = tau
        self.pred = None
        self.succ = None
        #self.prev = None
        #self.next = None

    def __eq__(self, other):
        return isinstance(other, DroneAction) and self.type == other.type and \
               self.x == other.x and  self.y == other.y and self.d == other.d and self.p == other.p # and self.pred == other.pred and self.succ == other.succ

    def __str__(self):
        id_pred = None
        id_succ = None
        #id_prev = None
        #id_next = None

        if self.pred is not None: id_pred = id(self.pred)
        if self.succ is not None: id_succ = id(self.succ)
        #if self.prev is not None: id_prev = id(self.prev)
        #if self.next is not None: id_next = id(self.next)

        return f"'id': {id(self)}, 'type':{self.type}, 'x': {self.x}, 'y': {self.y}, 'd': {self.d}, 'p': {self.p}, 'tau': {self.tau}, 'pred': {id_pred}, 'succ':{id_succ}" #, 'prev': {id_prev}, 'next':{id_next}"

    def getDICT(self):
        return {
            'type': self.type,
            'x': self.x,
            'y': self.y,
            'd': self.d,
            'p': self.p,
            'tau': self.tau
        }

    def getTime(self, simulation):
        if self.type == "move":
            return simulation.time(self.x, self.y)
        if self.type == "load":
            return LOAD_TIME
        if self.type == "unload":
            return UNLOAD_TIME
        if self.type == "swap":
            return SWAP_TIME
        return 0

    def getEnergyCost(self, simulation):
        if self.type == "move":
            w = 0
            if self.d is not None: w =  simulation.deliveries[self.d].weight
            return simulation.cost(self.x, self.y, w)
        return 0

