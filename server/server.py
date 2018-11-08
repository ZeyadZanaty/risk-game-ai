from flask import Flask, request, jsonify, session, g, current_app
from flask_cors import CORS
import numpy as np
import json
import math
from game import Game
from flask_session import Session
from uuid import uuid4

app = Flask(__name__)
CORS(app, supports_credentials=True)

game = {}

app.secret_key = 'okdok'

@app.route('/newGame', methods=['POST'])
def startGame():
    print(request.get_json())
    req = request.get_json()
    game_mode = req['gameMode']
    players_num = req['playersNum']
    map = req['map']
    session['game_id'] = uuid4()
    game_id = session['game_id']
    print(game_id)
    global game 
    game[game_id] = Game(map,game_mode,players_num)
    game[game_id].start()
    game_json = game[game_id].json()
    response = jsonify(game_json)
    return response

@app.route('/player/<id>', methods=['GET'])
def get_player(id):
    global game
    risk = game[session['game_id']]
    return jsonify(risk.players[int(id)].json())

@app.route('/territory/<name>', methods=['GET'])
def get_territory(name):
    global game
    risk = game[session['game_id']]
    return jsonify(next((x.json() for x in risk.territories if x.name == name), None))

@app.route('/player/territories/<id>', methods=['GET'])
def get_player_territories(id):
    global game
    risk = game[session['game_id']]
    res = {
        'territories':[t.json() for t in risk.players[int(id)].territories]
    }
    return jsonify(risk.players[int(id)].json())

@app.route('/attack',methods=['POST'])
def attack():
    global game
    game_id = session['game_id']
    print(request.get_json())
    req = request.get_json()
    attacker_id = req['attackerID']
    attackee_id = req['attackeeID']
    attacker_territory_name =  req['attackerTerritory']
    attackee_territory_name = req['attackeeTerritory']
    troops_num = req['troopsNum']
    if attackee_id is None:
        attackee_id = 0
    attacker_territory = next((x for x in game[game_id].territories if x.name == attacker_territory_name),None)
    attackee_territory = next((x for x in game[game_id].territories if x.name == attackee_territory_name),None)
    status,msg = game[game_id].players[int(attacker_id)].attack(game[game_id],
    troops_num,attacker_territory,game[game_id].players[int(attackee_id)],attackee_territory)
    game_json = game[game_id].json()
    game_json['attack'] ={"status":status,"msg":msg}
    response = jsonify(game_json)
    return response

@app.route('/pass/<id>', methods=['PUT'])
def pass_turn(id):
    global game
    game[session['game_id']].players[int(id)].pass_turn(game[session['game_id']])
    game_json = game[session['game_id']].json()
    response = jsonify(game_json)
    return response

@app.route('/reset', methods=['PUT'])
def reset_game():
    global game
    print(game)
    game.pop(session['game_id'],None)
    session.pop('game_id',None)
    print("Game Reset")
    return jsonify({})


if __name__ == '__main__':
    app.run(debug=True)





# from game import Game,GameMode

# game = Game("USA",GameMode.HUMAN_VS_HUMAN.value)
# game.start()

# print(game.players[0].json())
