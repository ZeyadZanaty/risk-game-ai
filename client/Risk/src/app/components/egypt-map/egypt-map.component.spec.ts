import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EgyptMapComponent } from './egypt-map.component';

describe('EgyptMapComponent', () => {
  let component: EgyptMapComponent;
  let fixture: ComponentFixture<EgyptMapComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EgyptMapComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EgyptMapComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
