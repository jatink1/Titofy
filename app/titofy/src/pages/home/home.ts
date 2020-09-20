import { Component, ViewChild, QueryList } from '@angular/core';
import { NavController } from 'ionic-angular';
import {
  StackConfig,
  // Stack,
  // Card,
  // ThrowEvent,
  DragEvent,
  SwingCardComponent,
  SwingStackComponent,
} from "angular2-swing";

import 'rxjs/Rx';
import { Http } from '@angular/http';

@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {

  @ViewChild("myswing1") swingStack: SwingStackComponent;
  @ViewChild("mycards1") swingCards: QueryList<SwingCardComponent>;

  public cards: any;
  stackConfig: StackConfig;
  recentCard: string = "";

  public count:number;

  constructor(public navCtrl: NavController,private http:Http) {
    // this.count = 0;
    // this.addNewCards(10);

    this.stackConfig = {
      throwOutConfidence: (offsetX, offsetY, element) => {
        return Math.min(Math.abs(offsetX) / (element.offsetWidth / 2), 1);
      },
      transform: (element, x, y, r) => {
        this.onItemMove(element, x, y, r);
      },
      throwOutDistance: (d) => {
        return 800;
      },
    };

  }//constructor ends here

  ngAfterViewInit() {
    // Either subscribe in controller or set in HTML
    this.swingStack.throwin.subscribe((event: DragEvent) => {
      event.target.style.background = "#ffffff";
    });

    this.cards = [{ email: "" ,name:""}];
    this.addNewCards(1);
  }

  onItemMove(element, x, y, r) {
    var color = "";
    var abs = Math.abs(x);
    let min = Math.trunc(Math.min(16 * 16 - abs, 16 * 16));
    let hexCode = this.decimalToHex(min, 2);

    if (x < 0) {
      color = "#FF" + hexCode + hexCode;
    } else {
      color = "#" + hexCode + "FF" + hexCode;
    }

    element.style.background = color;
    element.style[
      "transform"
    ] = `translate3d(0, 0, 0) translate(${x}px, ${y}px) rotate(${r}deg)`;
  }

  // Connected through HTML
  voteUp(like: boolean) {
    let removedCard = this.cards.pop();
    
      this.addNewCards(1);   
   
    
    if (like) {
      this.recentCard = "You liked: " + removedCard.name.first ;
      console.log(removedCard.name.first);
      
    } else {
      this.recentCard = "You disliked: " + removedCard.name.first;
    }
  }

  // Add new cards to our array
  async addNewCards(count: number) {
   this.http.get('https://randomuser.me/api/?results=' + count)
   .map((data)=>data.json().results)
      .subscribe(result => {
        for (let val of result) {
         
          this.cards.push(val);
        }
        console.log("Results", result);

      })
  }

  // http://stackoverflow.com/questions/57803/how-to-convert-decimal-to-hex-in-javascript
  decimalToHex(d, padding) {
    var hex = Number(d).toString(16);
    padding =
      typeof padding === "undefined" || padding === null
        ? (padding = 2)
        : padding;

    while (hex.length < padding) {
      hex = "0" + hex;
    }

    return hex;
  }



  myaccount(){
    this.navCtrl.push('MyaccountPage');
  }

  chats(){
    this.navCtrl.push('ChatsPage');
  }

}
