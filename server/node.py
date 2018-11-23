import numpy as np
import copy

class Node:
    def __init__(self, game, state, player, phase=0, parent=None, depth=0, path_cost=0, cost=0,prev_action=None):
        self.game = game
        self.state = copy.deepcopy(state)
        self.player = player
        self.parent = parent
        if self.parent is None:
            self.depth = depth
        else:
            self.depth = self.parent.depth+1
        self.cost = cost
        self.path_cost = path_cost
        self.phase = phase
        self.prev_action = prev_action
        self.update_state()

    def __lt__(self, other):
        return self.cost < other.cost

    def __repr__(self):
        return "Node(%s)" % (self.state)

    def __eq__(self, other):
        if isinstance(other, Node):
            return (self.state==other.state and self.phase==other.phase)
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash(self.__repr__())
    
    def decrease_key(self, frontier):
        for n in frontier:
            if self.state == n.state and self.phase == n.phase and self.cost < n.cost:
                self = copy.deepcopy(n)
                break

    def get_reinforce(self,trts,sorted_trts):
        children = []
        new_troops = max(3,len(trts) // 3)
        for trt in sorted_trts:
            children.append(Node(self.game,self.state,self.player,phase=1,parent=self,
            prev_action={'move_type':'reinforce','territory':trt.name,'troops':new_troops}))
        return children

    def get_attack(self,trts,sorted_trts):
        children = []
        for trt in sorted_trts:
            for other in trt.adjacent_territories:
                if other not in list(self.state[self.player.id].keys()):
                    troops = self.state[self.player.id][trt.name]-1
                    if troops >1:
                        for i in range(1,2):
                            attack_troops = troops // i
                            children.append(Node(self.game,self.state,self.player,parent=self,
                            phase=1,prev_action={'move_type':'attack','attacking':trt.name,'troops':attack_troops,'attacked':other,
                            'attacked_player': self.get_trt_occupier(other)}))
        children.append(Node(self.game,self.state,self.player,phase=0,parent=self,
        prev_action={'move_type':'end_turn'}))
        return children

    def get_neighbors(self,threshold):
        children = []
        trts = []
        sorted_trts = []
        for territory in list(self.state[self.player.id].keys()):
            trts.append(territory)
        trts.sort(key=lambda x: self.bsr(x), reverse = True)
        if self.phase == 0:
            sorted_trts = [self.game.get_territory(trt) for trt in trts if self.bsr(trt)>=threshold]
            children = self.get_reinforce(trts,sorted_trts)
        elif self.phase == 1:
            sorted_trts = [self.game.get_territory(trt) for trt in trts if self.bsr(trt)<=threshold]
            if len(sorted_trts) <= 0 or self.depth%7 == 0:
                children.append(Node(self.game,self.state,self.player,phase=0,parent=self,
        prev_action={'move_type':'end_turn'}))
            else:
                children = self.get_attack(trts,sorted_trts)
        return children

    def get_trt_occupier(self,territory):
        for p,trts in self.state.items():
            for trt in trts.keys():
                if trt == territory:
                    return p

    def calculate_heuristic(self):
        # self.heuristic = 0 
        # for trt in self.state[self.player.id].keys():
        #     self.heuristic+=1
        # other_troops = 0
        # my_troops = 0
        # for player_id,territories in self.state.items():
            # if player_id != self.player.id:
                # other_troops+=sum([troops for troops in list(territories.values())])
        #     if player_id == self.player.id:
        #         my_troops+=sum([troops for troops in list(territories.values())])            
        # self.heuristic  = (self.heuristic* my_troops)/other_troops
        # self.heuristic = len(self.state[self.player.id].items())
        self.heuristic = sum([self.bsr(trt) for trt in self.state[self.player.id].keys()])-(len(self.state[self.player.id].items())-len(self.game.territories.items()))

    def calculate_cost(self):
        self.calculate_heuristic()
        if self.parent is None:
            self.cost = self.heuristic
        else:
            self.path_cost = self.parent.path_cost + 1
            self.cost = self.path_cost + self.heuristic
            if self.prev_action and self.prev_action['move_type'] =='end_turn':
                self.cost+=3
    
    def update_state(self):
        previous_action = self.prev_action
        if previous_action == None:
            return
        elif previous_action['move_type'] == 'reinforce':
            self.state[self.player.id][previous_action['territory']]+=previous_action['troops']
        elif previous_action['move_type'] == 'attack':
            #attack logic
            attacking_troops = previous_action['troops']
            attacking_trt = previous_action['attacking']
            attacked_trt = previous_action['attacked']
            attacked_player = previous_action['attacked_player']
            attacked_troops = self.state[attacked_player][attacked_trt]
            if attacked_troops == 0 or attacking_troops>=attacked_troops:
                self.state[self.player.id][attacking_trt]-=attacking_troops
                self.state[self.player.id][attacked_trt] = attacking_troops
                self.state[attacked_player].pop(attacked_trt)
            elif attacking_troops < attacked_troops:
                self.state[attacked_player][attacked_trt]-=attacking_troops
        elif previous_action['move_type'] == 'end_turn':
            return

    def bsr(self,trt):
        get = getattr(self.game,'get_territory')
        bsr = sum([self.state[self.get_trt_occupier(territory)][territory] for territory in get(trt).adjacent_territories if self.get_trt_occupier(territory)!=self.player.id])
        bsr =  bsr / self.state[self.player.id][trt]
        return bsr

