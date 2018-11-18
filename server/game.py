import numpy as np
from player import Player
from territory import Territory
from troop import Troop
import random
from enum import Enum

starting_troops = 20
usa_states = {"Alabama":["Mississippi","Tennessee","Florida","Georgia"],
  "Alaska":["Hawaii","California","Arizona"],
  "Arizona":["California","Nevada","Utah","New Mexico"],
  "Arkansas":["Tennessee","Missouri","Oklahoma","Mississippi","Louisiana"],
  "California":["Nevada","Arizona","Alaska"],
  "Colorado":["Utah","Wyoming","Arizona","New Mexico","Nebraska","Kansas","Oklahoma"],
  "Connecticut":["New York","Rhode Island","Massachusetts"],
  "Delaware":["New Jersey","Maryland","Pennsylvania"],
  "Florida":["Alabama","Georgia"],
  "Georgia":["Florida","Alabama","South Carolina","Tennessee","North Carolina"],
  "Hawaii":["Alaska","Texas"],
  "Idaho":["Wyoming","Montana","Washington","Utah","Nevada","Oregon"],
  "Illinois":["Wisconsin","Iowa","Missouri","Indiana","Kentucky"],
  "Indiana":["Illinois","Michigan","Ohio","Kentucky"],
  "Iowa":["Wisconsin","Minnesota","Nebraska","Soth Dakota","Missouri"],
  "Kansas":["Nebraska","Oklahoma","Colorado","Missouri"],
  "Kentucky":["Indiana","Illinois","Virginia","Ohio","West Virginia","Tennessee","Missouri"],
  "Louisiana":["Arkansas","Texas","Mississippi"],
  "Maine":["New Hampshire"],
  "Maryland":["Delaware","Virginia","Pennsylvania","West Virginia"],
  "Massachusetts":["Vermont","New Hampshire","New York","Rhode Island","Connecticut"],
  "Michigan":["Indiana","Ohio","Wisconsin"],
  "Minnesota":["North Dakota","South Dakota","Iowa","Wisconsin"],
  "Mississippi":["Alabama","Arkansas","Louisiana","Tennessee"],
  "Missouri":["Kansas","Arkansas","Iowa","Illinois","Kentucky","Tennessee","Oklahoma"],
  "Montana":["Idaho","Wyoming","North Dakota","South Dakota"],
  "Nebraska":["Iowa","South Dakota","Wyoming","Colorado","Kansas","Missouri"],
  "Nevada":["Idaho","Utah","Arizona","California","Oregon"],
  "New Hampshire":["Maine","Vermont","Massachusetts"],
  "New Jersey":["Delaware","New York","Pennsylvania"],
  "New Mexico":["Oklahoma","Texas","Colorado","Utah","Arizona"],
  "New York":["Vermont","New Jersey","Pennsylvania","Massachusetts","Connecticut"],
  "North Carolina":["South Carolina","Virginia","Tennessee"],
  "North Dakota":["Montana","South Dakota","Minnesota"],
  "Ohio":["West Virginia","Indiana","Michigan","Kentucky"],
  "Oklahoma":["Texas","Kansas","Colorado","New Mexico","Arkansas","Missouri"],
  "Oregon":["Idaho","Washington","Nevada","California"],
  "Pennsylvania":["New York","Delaware","New Jersey","Maryland","Ohio","West Virginia"],
  "Rhode Island":["Massachusetts","Connecticut"],
  "South Carolina":["North Carolina","Gerogia"],
  "South Dakota":["North Dakota","Wyoming","Montana","Nebraska","Iowa","Minnesota"],
  "Tennessee":["North Carolina","Alabama","Mississippi","Georgia","Arkansas","Kentucky","Missouri"],
  "Texas":["New Mexicoa","Oklahoma","Arkansas","Louisiana","Hawaii"],
  "Utah":["Idaho","Nevada","Wyoming","Nevada","Colorado","New Mexico"],
  "Vermont":["New York","New Hampshire","Massachusetts"],
  "Virginia":["West Virginia","Maryland","North Carolina","Kentucky"],
  "Washington":["Oregon","Idaho"],
  "West Virginia":["Ohio","Virginia","Pennsylvania","Kentucky","Maryland"],
  "Wisconsin":["Michigan","Minnesota","Illinois","Iowa"],
  "Wyoming":["Montana","Idaho","Nebraska","Utah","Colorado","South Dakota"]}
egypt_states = {"Alexandria":["Beheira","Matruh"],
    "Aswan":["Red Sea","Luxor","New Valley"],
    "Asyut":["Minya","Sohag","New Valley","Red Sea","Qena"],
    "Beheira":["Alexandria","Kafr El Sheikh","Gharbia","Monufia","Giza"],
    "Beni Suef":["Minya","Giza","Faiyum","Red Sea"],
    "Cairo":["Giza","Suez","Qalyubia","Sharqia","Ismailia"],
    "Dakahlia":["Damietta","Port Said","Sharqia","Gharbia","Kafr El Sheikh"],
    "Damietta":["Dakahlia","Port Said"],
    "Faiyum":["Giza","Beni Suef"],
    "Gharbia":["Dakahlia","Kafr El Sheikh","Beheira","Monufia"],
    "Giza":["Faiyum","Suez","Beheira","Monufia","Qalyubia","Cairo","Matruh","New Valley","Red Sea"],
    "Ismailia":["North Sinai","Suez","Cairo","Sharqia","Port Said"],
    "Kafr El Sheikh":["Dakahlia","Beheira","Gharbia"],
    "Luxor":["Aswan","New Valley","Qena","Red Sea"],
    "Matruh":["Alexandria","Giza","Beheira","New Valley"],
    "Minya":["Beni Suef","Asyut","Giza","New Valley","Red Sea"],
    "Monufia":["Giza","Qalyubia","Qalyubia","Gharbia"],
    "New Valley":["Matruh","Giza","Minya","Asyut","Sohag","Qena","Luxor","Aswan"],
    "North Sinai":["South Sinai","Suez","Ismailia","Port Said"],
    "Port Said":["North Sinai","Dakahlia","Damietta","Sharqia","Ismailia"],
    "Qalyubia":["Giza","Sharqia","Monufia","Gharbia","Cairo"],
    "Qena":["Sohag","Luxor","Red Sea","New Valley"],
    "Red Sea":["Suez","Giza","Beni Suef","Minya","Asyut","Sohag","Qena","Luxor","Aswan"],
    "Sharqia":["Cairo","Ismailia","Suez","Qalyubia","Dakahlia","Port Said"],
    "Sohag":["Asyut","Qena","Red Sea","New Valley"],
    "South Sinai":["Suez","North Sinai"],
    "Suez":["Giza","Cairo","North Sinai","South Sinai","Sharqia","Ismailia"]}
colors = ['#346ac3','#d23c2f','#e1a904','#191919','#326f26','#764dbe']
class Game:

    def __init__(self,map,player_types,mode=0,players_num=2,player_turn=0,state=None):
        self.players_num = players_num
        self.mode = mode
        self.player_turn = player_turn
        self.state = state
        self.map = map
        self.player_types = player_types
    
    def start(self):
        self.generate_map()
        self.generate_players()
        self.generate_troops()
        self.update_state()

    def generate_map(self):
        self.territories = {}
        if self.map == 'USA':
            for state,adjacents in usa_states.items():
                self.territories[state]=Territory(state,adjacents)
        elif self.map == 'Egypt':
            for state,adjacents in egypt_states.items():
                self.territories[state]=Territory(state,adjacents)

    def generate_players(self):
        self.players = []
        for i in range(0,self.players_num):
            type = self.player_types[i]
            self.players.append(Player(i,colors[i],type=type))
            self.players[i].set_goal_state(self)

    def generate_troops(self):
        for i in range(0,starting_troops):
            for player in self.players:
                if player.troops is None:
                    player.troops=[]
                if player.territories is None:
                    player.territories = []
                troop = Troop(i,player,2)
                troop.assign_randomly(list(self.territories.values()))
                player.troops.append(troop)
    
    def get_territory(self,name):
        return self.territories[name]
    
    def update_state(self):
        if self.state is None:
            self.state ={}
        self.state = {trt.name:trt.occupying_player.id for trt in list(self.territories.values()) if trt.occupying_player}


    def json(self):
        return {
            "map":self.map,
            "mode":self.mode,
            "players_num":self.players_num,
            "player_turn":self.player_turn,
            "state":self.state,
            "players":[player.json() for player in self.players],
            "occupied_territories":[trty.json()  for trty in list(self.territories.values()) if trty.occupying_player],
            "territories":[trty.json() for trty in list(self.territories.values())]
        }

class GameMode(Enum):
    AI_VS_AI = 2
    HUMAN_VS_AI = 1
    HUMAN_VS_HUMAN = 0

class PlayerType(Enum):
    HUMAN = 0
    PASSIVE = 1
    AGRESSIVE = 2
    PACIFIST = 3
    GREEDY = 4
    ASTAR = 5
    ASTAR_REAL = 6
    MINIMAX = 7
