import numpy as np
from troop import Troop
starting_troops = 25
from agent import Agent 
import random
import copy

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
        if attacking_troops > len(my_territory.troops):
            attacking_troops = len(my_territory.troops)-1
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
            won = 0
            lost = 0
            attacking = copy.deepcopy(attacking_troops)
            while attacking_troops >0:
                attacker_dice = []
                defender_dice = []
                random.seed()
                attacker_dice=[random.randint(1, 6) for _ in range(0,min(3,attacking_troops))]
                attacker_dice.sort(reverse=True)
                defender_dice=[random.randint(1, 6) for _ in range(0,min(3,attacking_troops))]
                defender_dice.sort(reverse=True)
                print("DICE:",attacker_dice,defender_dice)
                for i in range(0,min(3,attacking_troops)):
                    if attacker_dice[i] > defender_dice[i] and other_territory.occupying_player is not self:
                        if len(other_territory.troops) > 0 :
                            troop = other_territory.troops.pop()
                            other_player.troops.remove(troop)
                            won+=1
                        if len(other_territory.troops) == 0:
                            self.territories.append(other_territory)
                            other_territory.occupying_player = self
                            other_player.territories.remove(other_territory)
                            for i in range(0,attacking-lost):
                                troop = my_territory.troops.pop()
                                self.troops.remove(troop)
                                new_troop = Troop(i,self,4)
                                new_troop.assign(game,other_territory.name)
                                self.troops.append(new_troop)
                            break
                    elif attacker_dice[i]<= defender_dice[i] and other_territory.occupying_player is not self:
                        if len(my_territory.troops)>0:
                            troop=my_territory.troops.pop()
                            self.troops.remove(troop)
                            lost+=1
                attacking_troops-=3 
            game.update_state()
            return True, "Won "+str(won)+" battle(s) and lost "+str(lost)+" troops"

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
        print(least,attackable)
        for adjacent in least.adjacent_territories:
            adj = game.get_territory(adjacent)
            if (adj in self.territories) and len(adj.troops)>1:
                return True,least,adj
            else: 
                if least in attackable:
                    attackable.remove(least)
        if attackable and len(attackable)>0:
            return self.get_pacifist_territory(game,attackable)  
        return False,None,None
    
    def init_agent(self,game):
        assert self.type in [4,5,6,7]
        if self.type == 4:
            agent_type = 'greedy'
            stochastic = False
        elif self.type == 5 :
            agent_type = 'a_star'
            stochastic = False
        elif self.type ==6:
            agent_type = 'id_a_star'
            stochastic = False
        elif self.type == 7:
            agent_type = 'minimax'
            stochastic = False
        self.agent = Agent(agent_type,game,self,stochastic)

    def run_agnet(self,reinforce_threshold,attack_threshold):
        if self.type == 4 or self.type == 5 or self.type == 6:
            self.moves = self.agent.run({'reinforce_threshold':reinforce_threshold,'attack_threshold':attack_threshold})
        turns = 0
        for move in self.moves[2]:
            if move and move['move_type']=="end_turn":
                turns+=1
        return self.moves,turns
            
    def get_move(self,game,reinforce_threshold,attack_threshold):
        attacks = []
        get = getattr(game,'get_territory')
        self.run_agnet(reinforce_threshold,attack_threshold)
        for move in self.moves[2]:
            print(move)
            if move:
                if move['move_type'] == 'end_turn':
                    break
                elif move['move_type'] == "reinforce":
                    troops_num=self.get_new_troops()
                    assinged_trt = move['territory']
                    self.assign_new_troops(game,{move['territory']:troops_num})
                elif move['move_type'] =="attack":
                    if move['attacked_player'] == -1:
                        move['attacked_player']=self.id
                    attack = list(self.attack(game,move['troops'],get(move['attacking'])
                    ,game.players[int(move['attacked_player'])],get(move['attacked'])))
                    attack.append(" attacked "+move['attacked']+" with "+move['attacking']+" ("+str(move['troops'])+") troops")
                    if attack[0]:
                        attacks.append(attack)
        self.pass_turn(game)
        return attacks,"placed troops in "+assinged_trt

        
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
