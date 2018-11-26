import numpy as np
import timeit
from queue import PriorityQueue
import copy
from node import Node
import sys

class Agent:
    #TODO define agent structure and figure out how to represnt possible moves/ heuristic funtions
    def __init__(self,type,game,player,stochastic=False):
        self.type = type
        self.game = game
        self.player = player
        self.stochastic = stochastic

    def run(self,params={}):
        agent_call = getattr(self,self.type)
        if agent_call:
            return agent_call(**params)
    
    def get_path(self,goal_node):
        print(goal_node.state)
        path = []
        while goal_node.parent != None:
            path.insert(0, goal_node.prev_action)
            goal_node = goal_node.parent
        return path
    
    def a_star(self, reinforce_threshold=1,attack_threshold=2):
        start = timeit.default_timer()
        root = Node(self.game,self.game.state, self.player,stochastic=self.stochastic)
        frontier = PriorityQueue()
        frontier.put(root, root.cost)
        frontier_set = set()
        frontier_set.add(root)
        visited = set()
        while not frontier.empty():
            node = frontier.get()
            frontier_set.remove(node)
            move = node.prev_action['move_type'] if node.prev_action else None
            print("\n","player:",self.player.id,"depth:",node.depth,"territories:",len(node.state[self.player.id].items()),"move:",move,"cost:",node.cost,"visitied:",len(visited))
            visited.add(node)
            # get_nps(start, visited)
            if self.goal_test(node):
                stop = timeit.default_timer()
                return True,stop-start,self.get_path(node)
            if self.semi_goal_test(node) and timeit.default_timer()-start>60:
                stop = timeit.default_timer()
                return True,stop-start,self.get_path(node)
            for n in node.get_neighbors(reinforce_threshold,attack_threshold):
                n.calculate_cost()
                if n not in visited and n not in frontier_set:
                    frontier.put(n, n.cost)
                    frontier_set.add(n)
                else:
                    n.decrease_key(frontier.queue)
        stop = timeit.default_timer()    
        return False,stop-start,self.get_path(node)
    
    def greedy(self, reinforce_threshold=1,attack_threshold=2):
        start = timeit.default_timer()
        root = Node(self.game,self.game.state, self.player,stochastic=self.stochastic)
        root.calculate_heuristic()
        frontier = PriorityQueue()
        frontier.put(root, root.heuristic)
        frontier_set = set()
        frontier_set.add(root)
        visited = set()
        while not frontier.empty():
            node = frontier.get()
            frontier_set.remove(node)
            move = node.prev_action['move_type'] if node.prev_action else None
            print("\n","player:",self.player.id,"depth:",node.depth,"territories:",len(node.state[self.player.id].items()),'move:',move,"cost:",node.heuristic,"visitied:",len(visited))
            visited.add(node)
            # get_nps(start, visited)
            if self.goal_test(node):
                stop = timeit.default_timer()
                return True,start-stop,self.get_path(node)
            for n in node.get_neighbors(reinforce_threshold,attack_threshold):
                n.calculate_heuristic()
                if n not in visited and n not in frontier_set:
                    frontier.put(n, n.heuristic)
                    frontier_set.add(n)
                else:
                    n.decrease_key(frontier.queue)
        stop = timeit.default_timer()    
        return False,stop-start,self.get_path(node)

    def goal_test(self,node):
        return len(node.state[self.player.id].values()) == len(self.game.territories.items())

    def semi_goal_test(self,node):
        if self.game.map =='Egypt':
            return len(node.state[self.player.id].values()) == len(self.game.territories.items())-1 or len(node.state[self.player.id].values()) == len(self.game.territories.items())-2 or len(node.state[self.player.id].values()) == len(self.game.territories.items())-3
        if self.game.map =='USA':
            return len(node.state[self.player.id].values()) == len(self.game.territories.items())-1 or len(node.state[self.player.id].values()) == len(self.game.territories.items())-3 or len(node.state[self.player.id].values()) == len(self.game.territories.items())-4 or len(node.state[self.player.id].values()) == len(self.game.territories.items())-5 or len(node.state[self.player.id].values()) == len(self.game.territories.items())-6 or len(node.state[self.player.id].values()) == len(self.game.territories.items())-7

    def id_a_star(self,reinforce_threshold=1,attack_threshold=2):
        start = timeit.default_timer()
        root = Node(self.game,self.game.state, self.player,stochastic=self.stochastic)
        root.calculate_heuristic()
        bound = root.heuristic
        if self.game.map =='USA':
            minimum = 200
        else: minimum = 100
        while True:
            t,path = self.search(root,0, bound,reinforce_threshold,attack_threshold,start)
            if t == 'FOUND':
                stop = timeit.default_timer()
                return True,stop-start,path,
            if t == minimum:
                stop = timeit.default_timer()
                return False,stop-start,path
            bound = t

    def search(self, node,g, bound, reinforce_threshold,attack_threshold,start):
        path = []
        node.cost = g+node.heuristic
        move = node.prev_action['move_type'] if node.prev_action else None
        print("\n","player:",self.player.id,"depth:",node.depth,"territories:",len(node.state[self.player.id].items()),"move:",move,"cost:",node.cost,"time:",int(timeit.default_timer()-start))
        if node.cost > bound:
            return node.cost,path
        if self.goal_test(node):
            return 'FOUND',path
        if self.semi_goal_test(node) and timeit.default_timer()-start>15:
            return 'FOUND',path
        if self.game.map =='USA':
            minimum = 200
        else: minimum = 100
        for neighbour in node.get_neighbors(reinforce_threshold,attack_threshold):
            neighbour.calculate_heuristic()
            t,path = self.search(neighbour,g+1, bound,reinforce_threshold,attack_threshold,start)
            if t == 'FOUND':
                path.insert(0, node.prev_action)
                return 'FOUND',path
            if t < minimum:
                minimum = t
        return minimum,path