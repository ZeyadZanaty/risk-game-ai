import numpy as np
class Territory:

    def __init__(self,name,adjacent_territories,occupying_player=None,troops=None):
        self.name = name
        self.adjacent_territories = adjacent_territories
        self.occupying_player = occupying_player
        self.troops = troops

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def get_bsr(self,game):
        get = getattr(game,'get_territory')
        self.bsr = sum([len(get(territory).troops) for territory in self.adjacent_territories if get(territory).troops]) / len(self.troops)
        return self.bsr

    def get_nbsr(self,game):
        self.nbsr = self.get_bsr(game) / sum([trt.get_bsr(game) for trt in self.occupying_player.territories])
        return self.nbsr

    def json(self):
        return {
            "name":self.name,
            "adjacent_territories":self.adjacent_territories,
            "occupying_player":self.occupying_player.id if self.occupying_player else None,
            "troops": [troop.json() for troop in self.troops] if self.occupying_player else None
        }
    def print(self):
        print("Territory",self.name," occupied by player",self.occupying_player.id,
        "with",len(self.troops),"troops")

