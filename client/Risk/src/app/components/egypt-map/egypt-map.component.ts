import { Component, OnInit,Input,Output,EventEmitter } from '@angular/core';
import {MessageService} from 'primeng/api';

@Component({
  selector: 'app-egypt-map',
  templateUrl: './egypt-map.component.html',
  styleUrls: ['./egypt-map.component.css'],
  providers: [MessageService]

})
export class EgyptMapComponent implements OnInit {

  @Input() attackerTerritories;
  @Input() attackableTerritories;
  @Output() attackingTerritoryChange = new EventEmitter<string>();
  @Output() attackeeTerritoryChange = new EventEmitter<string>();
  @Output() currentTerritoryChange = new EventEmitter<any>();
  @Input() adjacent_territories;
  attackingTerritory:string;
  attackeeTerritory:string;
  @Input() allTerritories = [];
  currentTerritory:any;
  colors=['red','blue','green'];
  constructor(private messageService: MessageService) { }

  ngOnInit() {
  }

  onSelect(territory){
    if(this.attackerTerritories.indexOf(territory)!=-1){
      this.attackingTerritoryChange.emit(territory);
      this.attackingTerritory = territory;
    }
    else if(this.adjacent_territories.indexOf(territory)!=-1){
      this.attackeeTerritoryChange.emit(territory);
      this.attackeeTerritory = territory;
    }
    else{
      this.messageService.add({severity:'error', summary: "Terrritory Unusable", detail:"Please select another one.."});
    }
  }

  getTroops(territory){
  let current = this.allTerritories.filter(x =>x.name ==territory);
  if(current[0] && current[0].troops)
    return current[0].troops.length
  }

  onHover(event,territory){
    if(this.allTerritories.length!=0){
    this.currentTerritory = this.allTerritories.filter(x =>x.name ==territory)[0];
    this.currentTerritoryChange.emit(this.currentTerritory);
    }
  }

  onLeave(){
    if(this.allTerritories.length!=0){
    this.currentTerritory = null;
    this.currentTerritoryChange.emit(null);
    }
  }
  
  getColor(territory){
    if(this.allTerritories.length!=0){
    let trt = this.allTerritories.filter(x =>x.name ==territory)[0];
    if(trt&&trt.occupying_player!=null){
      return this.colors[trt.occupying_player];
    }
    else return 'transparent';
    }
    else return 'transparent';
  }

}
