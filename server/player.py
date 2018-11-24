import numpy as np
from troop import Troop
starting_troops = 25
from agent import Agent 

class Player:

    def __init__(self,id,color,troops=None,score=0,territories=None,type=0):
        self.troops = troops
        self.score = score
        self.id = id
        self.color = color
        self.type = type
        self.territories = territories
        self.moves = None

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def set_goal_state(self,game):
        self.goal_state = [self.id for trt in list(game.territories.items())]

    def attack(self,game,attacking_troops,my_territory,other_player,other_territory):
        if my_territory not in self.territories:
            return False, "Selected territory is not yours"
        elif other_territory.name not in my_territory.adjacent_territories:
            return False, "Territory "+other_territory.name+" is not adjacent to "+my_territory.name
        elif len(my_territory.troops) == 1:
            return False, "You can't attack with your only troop"
        elif attacking_troops - len(my_territory.troops) == 0:
            return False, "Leave no man behind"
        elif other_territory.occupying_player is None:
            other_territory.occupying_player = self
            self.territories.append(other_territory)
            other_territory.troops = []
            for i in range (0,attacking_troops):
                troop = my_territory.troops.pop()
                self.troops.remove(troop)
                new_troop = Troop(i,self,4)
                new_troop.assign(game,other_territory.name)
                self.troops.append(new_troop)
            game.update_state()
            return True, "That was easy"
        else:
            other_troops = len(other_territory.troops)
            if attacking_troops >= other_troops:
                for i in range(0,len(other_territory.troops)):
                    troop = other_territory.troops.pop()
                    other_player.troops.remove(troop)
                other_player.territories.remove(other_territory)
                self.territories.append(other_territory)
                other_territory.occupying_player = self
                for i in range(0,attacking_troops):
                    troop = my_territory.troops.pop()
                    self.troops.remove(troop)
                    new_troop = Troop(i,self,4)
                    new_troop.assign(game,other_territory.name)
                    self.troops.append(new_troop)
            elif attacking_troops < other_troops:
                for i in range(0,attacking_troops):
                    troop = other_territory.troops.pop()
                    other_player.troops.remove(troop)
            game.update_state()
            return True, "You win the battle, but not the war"

    def pass_turn(self,game):
        game.player_turn = (game.player_turn+1) % game.players_num
        game.update_state()

    def get_reinforcemnets(self,territories):
        number_of_troops = int(len(self.territories)/3)
        if number_of_troops <3:
            number_of_troops = 3
        for i in range(0,number_of_troops):
            troop = Troop(i,self,2)
            troop.assign_randomly(territories)
            self.troops.append(troop)
    
    def get_new_troops(self):
        return max(3,len(self.territories) // 3)

    def assign_new_troops(self,game,assigned_territories):
        for territory,troops in assigned_territories.items():
            for i in range(0,troops):
                troop = Troop(i,self,3)
                troop.assign(game,territory)
                self.troops.append(troop)

    def get_attackable_territories(self,game):
        attackable_territories = []
        for territory in self.territories:
            for adjacent in territory.adjacent_territories:
                adjacent_trt = game.get_territory(adjacent)
                if adjacent_trt not in attackable_territories and adjacent_trt not in self.territories:
                    attackable_territories.append(adjacent_trt)
        if attackable_territories:
            return attackable_territories
        else: return []
    
    def get_attackable(self,game):
        attackable ={}
        for trt in self.territories:
            if len(trt.troops)>1:
                trts = []
                for adjacent in trt.adjacent_territories:
                    adj = game.get_territory(adjacent)
                    if adj not in trts and adj not in self.territories:
                        trts.append(adj)
                attackable[trt] = trts
    
    def can_attack(self,my_territory,other_territory):
        if len(my_territory.troops)<=1 or other_territory in self.territories:
            return False
        return True

    def attack_passive(self,game):
        troops_num=self.get_new_troops()
        least_troops_trt = min(self.territories,key=lambda x: len(x.troops))
        self.assign_new_troops(game,{least_troops_trt.name:troops_num})
        self.pass_turn(game)
        return True,"placed troops in "+least_troops_trt.name+" and made no attacks!"
    
    def attack_aggressive(self,game):
        troops_num=self.get_new_troops()
        max_troops_trt = max(self.territories,key=lambda x: len(x.troops) if x.troops else 0)
        self.assign_new_troops(game,{max_troops_trt.name:troops_num})
        attacks = self.get_aggressive_attacks(game)
        self.pass_turn(game)
        return attacks,"placed troops in "+max_troops_trt.name

    def get_aggressive_attacks(self,game):
        attacks = []
        for trt in self.territories:
            for adj in trt.adjacent_territories:
                other_trt = game.get_territory(adj)
                if self.can_attack(trt,other_trt):
                    troops = len(trt.troops)-1
                    attack = list(self.attack(game,troops,trt,other_trt.occupying_player,other_trt))
                    attack.append(" attacked "+other_trt.name+" with "+trt.name+" ("+str(troops)+") troops")
                    attacks.append(attack)
        return attacks
    
    def attack_pacifist(self,game):
        troops_num=self.get_new_troops()
        least_troops_trt = min(self.territories,key=lambda x: len(x.troops) if x.troops else 0)
        self.assign_new_troops(game,{least_troops_trt.name:troops_num})
        attackable = self.get_attackable_territories(game)
        if attackable is None or len(attackable)==0:
            self.pass_turn(game)
            return False,'No attackable territories',''
        stat, other_territory, my_territory = self.get_pacifist_territory(game,attackable)
        if not stat:
            self.pass_turn(game)
            return True,'',"placed troops in "+least_troops_trt.name+" but couldn't find a territory to attack"
        attacking_troops = len(my_territory.troops)-1
        if other_territory.occupying_player:
            other_player = game.players[other_territory.occupying_player.id]
        else:
            other_player = self
        attack,msg = self.attack(game,attacking_troops,my_territory,other_player,other_territory)
        if attack:
            self.pass_turn(game)
            return attack,msg,"placed troops in "+least_troops_trt.name+" and attacked "+other_territory.name+" with "+my_territory.name
        else:
            self.pass_turn(game)
            return attack,msg,""

    def get_pacifist_territory(self,game,attackable):
        least = min(attackable,key=lambda x:len(x.troops) if x.troops else 0)
        for adjacent in least.adjacent_territories:
            adj = game.get_territory(adjacent)
            if (adj in self.territories) and len(adj.troops)>1:
                return True,least,adj
        return False,None,None
    
    def init_agent(self,game):
        assert self.type in [4,5,6,7]
        if self.type == 4:
            agent_type = 'greedy'
        elif self.type == 5 or self.type == 6:
            agent_type = 'a_star'
        elif self.type == 7:
            agent_type = 'minimax'
        self.agent = Agent(agent_type,game,self)

    def run_agnet(self,reinforce_threshold,attack_threshold):
        self.moves = self.agent.run({'reinforce_threshold':reinforce_threshold,'attack_threshold':attack_threshold})
        turns = 0
        for move in self.moves[2]:
            if move['move_type']=="end_turn":
                turns+=1
        return self.moves,turns
            
        
    def json(self):
        return {
            "id":self.id,
            "color":self.color,
            "troops":[troop.json() for troop in self.troops],
            "territories":[trty.json() for trty in self.territories],
            "score":self.score,
            "type":self.type,
            "goal":self.goal_state,
            "moves":self.moves
            }

    def print(self):
        print("Player",self.id,
        "No of troops=",len(self.troops),
        "No of territories=",len(self.territories))
