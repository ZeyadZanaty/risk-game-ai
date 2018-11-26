import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import 'rxjs/add/operator/map';
import 'rxjs/Rx';

@Injectable({
  providedIn: 'root'
})
export class GameService {

  serverUrl:string = "http://127.0.0.1:5000/";
  private httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
    withCredentials: true // to allow cookies to go from "https://localhost:4567" to "http://localhost:5678"
  };
  constructor(private _http: HttpClient) {}

  createGame(game){
    return this._http.post(this.serverUrl+'newGame',game, this.httpOptions)
  }
  resetGame(game){
    return this._http.put(this.serverUrl+'reset',game)
  }

  getPlayer(id){
    return this._http.get(this.serverUrl+'player/'+id, this.httpOptions)
  }

  getTerritory(name){
    return this._http.get(this.serverUrl+'territory/'+name, this.httpOptions)
  }

  getPlayerTerritories(id){
    return this._http.get(this.serverUrl+'player/territories/'+id,this.httpOptions)
  }

  passTurn(id,game){
    return this._http.put(this.serverUrl+'pass/'+id,game,this.httpOptions).toPromise();
  }

  attack(attack){
    return this._http.post(this.serverUrl+'attack',attack,this.httpOptions).toPromise();
  }

  joinGame(id){
    return this._http.get(this.serverUrl+'join/'+id,this.httpOptions)
  }

  getNewTroopsNum(gameid){
    return this._http.get(this.serverUrl+'troopsNum/'+gameid,this.httpOptions)
  }

  assignNewTroops(id,dict){
    return this._http.post(this.serverUrl+'troops/assign/'+id,dict, this.httpOptions)
  }
  attackPassive(playerid,game){
    return this._http.put(this.serverUrl+'attack/passive/'+playerid,game,this.httpOptions).toPromise();
  }

  attackAggressive(playerid,game){
    return this._http.put(this.serverUrl+'attack/aggressive/'+playerid,game,this.httpOptions).toPromise();
  }

  attackPacifist(playerid,game){
    return this._http.put(this.serverUrl+'attack/pacifist/'+playerid,game,this.httpOptions).toPromise();
  }
  
  attackAgent(playerid,game){
    return this._http.put(this.serverUrl+'attack/agent/'+playerid,game,this.httpOptions).toPromise();
  }

}
