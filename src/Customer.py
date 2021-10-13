class Customer:
    def __init__(self, ID, sim):
        assert type(ID) == int
        self.SIMULATION = sim
        self.ID = ID

    '''def requestDelivery(self, src_id, dst_id, budget):
        self.SIMULATION.receiveRequest(src_id, dst_id, budget)'''

    def printInfo(self):
        print(f"customer ID: {self.ID}")