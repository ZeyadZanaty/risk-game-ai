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
  resetGame(){
    return this._http.put(this.serverUrl+'reset',{})
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

  passTurn(id){
    return this._http.put(this.serverUrl+'pass/'+id,this.httpOptions)
  }
  attack(attack){
    return this._http.post(this.serverUrl+'attack',attack,this.httpOptions)
  }
}
