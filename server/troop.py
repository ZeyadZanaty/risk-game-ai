import numpy as np
import random

class Troop:

    def __init__(self,id,player,value,territory=None):
        self.territory = territory
        self.player = player
        self.value = value
        self.id = id
    
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def assign_to_territory(self,territories):
        while self.territory is None:
            trt = random.choice(territories)
            if trt.occupying_player is None:
                self.player.territories.append(trt)
                self.territory = trt  
                trt.occupying_player = self.player
                if trt.troops is None:
                    trt.troops = []
                    trt.troops.append(self)
                else:
                    trt.troops.append(self)
            elif trt.occupying_player == self.player: 
                self.territory = trt
                trt.troops.append(self)  
    
    def json(self):
        return {
            "id":self.id,
            "territory":self.territory.name,
            "player":self.player.id,
            "value":self.value
        }
    
    def print(self):
        print("Troop",self.id,"serving player",self.player.id,"occupying",self.territory.name)
     

        

