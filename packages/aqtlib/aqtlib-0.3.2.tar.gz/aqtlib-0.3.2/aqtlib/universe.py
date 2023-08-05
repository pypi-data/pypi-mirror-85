class Universe:
    def __init__(self, name, broker=None, porter=None):
        self.name = name
        self.broker = broker
        self.porter = porter

    def __repr__(self):
        return f'IBGW Universe ({self.name})'

    @property
    def SP500(self):
        pass

    @property
    def Russle2000(self):
        pass
