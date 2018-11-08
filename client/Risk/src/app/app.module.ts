import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import {InputTextModule} from 'primeng/inputtext';
import {ButtonModule} from 'primeng/button';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { HttpModule } from '@angular/http';
import { httpInterceptorProviders } from './http-interceptors/index';

// import { AppRoutingModule } from './/app-routing.module';
import { AppComponent } from './app.component';
import { UsaMapComponent } from './components/usa-map/usa-map.component';
import { EgyptMapComponent } from './components/egypt-map/egypt-map.component';
import { GameComponent } from './components/game/game.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule } from '@angular/forms';
import {TooltipModule} from 'primeng/tooltip';
import {SidebarModule} from 'primeng/sidebar';
import {RadioButtonModule} from 'primeng/radiobutton';
import {DialogModule} from 'primeng/dialog';
import {ConfirmDialogModule} from 'primeng/confirmdialog';
import {InputMaskModule} from 'primeng/inputmask';
import {SliderModule} from 'primeng/slider';
import {SelectButtonModule} from 'primeng/selectbutton';
import {TabViewModule} from 'primeng/tabview';
import {BlockUIModule} from 'primeng/blockui';
import {ProgressSpinnerModule} from 'primeng/progressspinner';
import {DropdownModule} from 'primeng/dropdown';
import {ToastModule} from 'primeng/toast';
import {SpinnerModule} from 'primeng/spinner';

@NgModule({
  declarations: [
    AppComponent,
    UsaMapComponent,
    EgyptMapComponent,
    GameComponent
  ],
  imports: [
    BrowserModule,
    // AppRoutingModule,
    BrowserAnimationsModule,
    ConfirmDialogModule,
    FormsModule,
    InputTextModule,
    ButtonModule,
    TooltipModule,
    SidebarModule,
    RadioButtonModule,
    DialogModule,
    HttpModule,
    HttpClientModule,
    InputMaskModule,
    SliderModule,
    SelectButtonModule,
    BrowserAnimationsModule,
    FormsModule,
    ButtonModule,
    TabViewModule,
    BlockUIModule,
    ProgressSpinnerModule,
    DropdownModule,
    ToastModule,
    SpinnerModule
  ],
  providers: [httpInterceptorProviders],
  bootstrap: [AppComponent]
})
export class AppModule { }
