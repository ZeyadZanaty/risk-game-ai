import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { UsaMapComponent } from './usa-map.component';

describe('UsaMapComponent', () => {
  let component: UsaMapComponent;
  let fixture: ComponentFixture<UsaMapComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ UsaMapComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UsaMapComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
