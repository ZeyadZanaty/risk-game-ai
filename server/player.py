import numpy as np
from troop import Troop
starting_troops = 20

class Player:

    def __init__(self,id,color,troops=None,score=0,territories=None):
        self.troops = troops
        self.score = score
        self.id = id
        self.color = color
        self.territories = territories

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


    def attack(self,game,attacking_troops,my_territory,other_player,other_territory):
        if my_territory not in self.territories:
            return False, "Selected territory is not yours"
        elif other_territory.name not in my_territory.adjacent_territories:
            return False, "Territory is not adjacent"
        elif len(my_territory.troops) == 1:
            return False, "Leave no man behind"
        elif attacking_troops - len(my_territory.troops) == 0:
            return False, "Leave no man behind"
        elif other_territory.occupying_player is None:
            other_territory.occupying_player = self
            self.territories.append(other_territory)
            other_territory.troops = []
            for i in range (0,attacking_troops):
                troop = my_territory.troops.pop()
                other_territory.troops.append(troop)
            # self.get_reinforcemnets(game.territories)
            game.player_turn = (game.player_turn+1) % game.players_num
            return True, "That was easy"
        else:
            other_troops = len(other_territory.troops)
            if attacking_troops > other_troops:
                other_player.territories.remove(other_territory)
                self.territories.append(other_territory)
                other_territory.occupying_player = self
                other_territory.troops = []
                for i in range(0,attacking_troops-other_troops):
                    troop = my_territory.troops.pop()
                    troop.territory = other_territory
                    other_territory.troops.append(troop)
            elif attacking_troops == other_troops:
                other_territory.occupying_player = None
                other_territory.troops = None
            elif attacking_troops < other_troops:
                for i in range(0,other_troops-attacking_troops):
                    other_territory.troops.pop()
            # self.get_reinforcemnets(game.territories)
            game.player_turn = (game.player_turn+1) % game.players_num
            return True, "You win the battle, but not the war"

    def pass_turn(self,game):
        game.player_turn = (game.player_turn+1 )%game.players_num
        self.get_reinforcemnets(game.territories)

    def get_reinforcemnets(self,territories):
        number_of_troops = int(len(self.territories)/3)
        if number_of_troops <3:
            number_of_troops = 3
        for i in range(0,number_of_troops):
            troop = Troop(i,self,2)
            troop.assign_to_territory(territories)
            self.troops.append(troop)
    
    def get_new_troops(self):
        number_of_troops = int(len(self.territories)/3)
        if number_of_troops <3:
            number_of_troops = 3
        return number_of_troops

    def assign_new_troops(self,game,assigned_territories):
        for territory,troops in assigned_territories.items():
            for i in range(0,troops):
                troop = Troop(i,self,3)
                troop.assign(game,territory)
                self.troops.append(troop)
    

    def json(self):
        return {
            "id":self.id,
            "color":self.color,
            "troops":[troop.json() for troop in self.troops],
            "territories":[trty.json() for trty in self.territories],
            "score":self.score
            }

    def print(self):
        print("Player",self.id,
        "No of troops=",len(self.troops),
        "No of territories=",len(self.territories))
