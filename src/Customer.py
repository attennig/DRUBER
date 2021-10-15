class Customer:
    def __init__(self, ID):
        assert type(ID) == int
        self.ID = ID

    '''def requestDelivery(self, src_id, dst_id, budget):
        self.SIMULATION.receiveRequest(src_id, dst_id, budget)'''

    def printInfo(self):
        print(f"customer ID: {self.ID}")