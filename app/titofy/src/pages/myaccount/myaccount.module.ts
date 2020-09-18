import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { MyaccountPage } from './myaccount';

@NgModule({
  declarations: [
    MyaccountPage,
  ],
  imports: [
    IonicPageModule.forChild(MyaccountPage),
  ],
})
export class MyaccountPageModule {}
