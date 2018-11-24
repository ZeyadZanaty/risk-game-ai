import numpy as np
import timeit
from queue import PriorityQueue
import copy
from node import Node

class Agent:
    #TODO define agent structure and figure out how to represnt possible moves/ heuristic funtions
    def __init__(self,type,game,player):
        self.type = type
        self.game = game
        self.player = player

    def run(self,params={}):
        agent_call = getattr(self,self.type)
        if agent_call:
            return agent_call(**params)
    
    def get_path(self,goal_node):
        path = []
        while goal_node.parent != None:
            path.insert(0, goal_node.prev_action)
            goal_node = goal_node.parent
        return path
    
    def a_star(self, reinforce_threshold=1,attack_threshold=2):
        start = timeit.default_timer()
        root = Node(self.game,self.game.state, self.player)
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
        root = Node(self.game,self.game.state, self.player)
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


    