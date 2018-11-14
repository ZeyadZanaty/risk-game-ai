import { Component, OnInit } from '@angular/core';
import { GameService } from '../../services/game.service'

@Component({
  selector: 'app-usa-map',
  templateUrl: './usa-map.component.html',
  styleUrls: ['./usa-map.component.css']
})
export class UsaMapComponent implements OnInit {
  
  constructor(private gameService:GameService) { }

  ngOnInit() {
  }

  getTerritory(state){
    this.gameService.getTerritory(state).subscribe(t=>console.log(t));
  }
}
