import { Component, OnInit } from '@angular/core';
import { GameService } from '../../services/game.service'
import {MessageService} from 'primeng/api';

@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.css'],
  providers: [MessageService]
})
export class GameComponent implements OnInit {

  map:string = 'Egypt';
  playersNum:number = 2;
  gameMode:number = 0;
  territories:any[];
  maps:any[];
  gameModes:any[];
  numberOptions:any[];
  gameStarted:boolean = false;
  game:any;
  currentPlayer:any;
  currentAdjacents:any=[];
  attackerTerritories:any=[];
  attackableTerritories:any=[];
  attackingTerritory:any;
  attackeeTerritory:any;
  attackingTroopsNum:number;
  constructor(private gameService:GameService,private messageService: MessageService) { }

  ngOnInit() {
    this.maps = [
          {label:'🇺🇸 USA', value:'USA'},
          {label:'🇪🇬 Egypt', value:'Egypt'}
      ];
    this.gameModes = [
          {label:'Human vs Human', value:0},
          {label:'Human vs AI', value:1},
          {label:'AI vs AI', value:2}
      ];
    this.numberOptions = [
          {label:'2', value:2},
          {label:'3', value:3},
          {label:'4', value:4},
          {label:'5', value:5},
          {label:'6', value:6},

      ];
    this.game={'territories':[]}
  }

  startGame(){
    this.gameStarted = true;
    let newGame = {"map":this.map,"gameMode":this.gameMode,"playersNum":this.playersNum}
    this.gameService.createGame(newGame)
    .subscribe(game=>{
      this.game = game
      console.log(game);
      this.currentPlayer = this.game.players[this.game.player_turn];
      this.getAttackerTerritories(this.currentPlayer);
    });
  }

  resetGame(){
    this.gameStarted = false;
    this.gameService.resetGame().subscribe(n=>{
      this.attackerTerritories =[];
      this.attackableTerritories =[];
    });
  }

  getAttackerTerritories(player){
    this.attackerTerritories =[]
    for(let tr of player.territories){
      this.attackerTerritories.push(tr.name);
    }
    this.attackableTerritories = [];
    setTimeout(()=>{
    for(let t of player.territories){
      for(let tr of t.adjacent_territories){
        if (this.attackableTerritories.indexOf(tr) ==-1 &&this.attackerTerritories.indexOf(tr)==-1){
          this.attackableTerritories.push(tr);
        }
      }
    }},200)
  }

  onAttacking(territory){
    this.attackeeTerritory = null;
    for(let t of this.currentPlayer.territories){
      if(territory == t.name){
        this.currentAdjacents = t.adjacent_territories;
        this.attackingTerritory=t;
      }
    }
    this.attackableTerritories = [];
    setTimeout(()=>{
    for(let t of this.attackingTerritory.adjacent_territories){
      if(this.attackerTerritories.indexOf(t)==-1){
        console.log(t)
        this.attackableTerritories.push(t);
      }
    }},200)
  }

  onAttackee(territory){
    for(let t of this.game.territories){
      if(territory == t.name){
        this.attackeeTerritory=t;
      }
    }
  }
  onPass(){
    this.gameService.passTurn(this.currentPlayer.id)
    .subscribe(game=>{
      this.game = game;
      console.log(game);
      this.currentPlayer = this.game.players[this.game.player_turn];
      this.getAttackerTerritories(this.currentPlayer);
      this.messageService.add({severity:'info', summary: 'Turn Passed', detail:"You've passed your turn"});
    });
    setTimeout(()=>this.attackeeTerritory=null,100);
    setTimeout(()=>this.attackingTerritory=null,100);
  }

  onAttack(){
    let attack ={
      "attackerID":this.currentPlayer.id,
      "attackeeID":this.attackeeTerritory.occupying_player,
      "attackerTerritory":this.attackingTerritory.name,
      "attackeeTerritory":this.attackeeTerritory.name,
      "troopsNum":this.attackingTroopsNum
    }
    this.gameService.attack(attack)
    .subscribe(game=>{
      this.game = game;
      console.log(game);
      this.currentPlayer = this.game.players[this.game.player_turn];
      this.getAttackerTerritories(this.currentPlayer);
      if(this.game.attack.status==true)
      this.messageService.add({severity:'success', summary: 'Attack successful', detail:this.game.attack.msg});
      if(this.game.attack.status==false)
      this.messageService.add({severity:'error', summary: 'Attack failed', detail:this.game.attack.msg});
    });
    setTimeout(()=>this.attackeeTerritory=null,100);
    setTimeout(()=>this.attackingTerritory=null,100);
    setTimeout(()=>this.attackingTroopsNum=1,100);
  }

}
