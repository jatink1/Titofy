import { Component } from "@angular/core";
import { IonicPage, NavController, NavParams } from "ionic-angular";
import { FormGroup, AbstractControl, FormBuilder, Validators } from "@angular/forms";

@IonicPage()
@Component({
  selector: "page-login",
  templateUrl: "login.html",
})
export class LoginPage {
  userLogin: FormGroup;
  femail: AbstractControl;
  fpassword: AbstractControl;

  constructor(
    public navCtrl: NavController,
    public navParams: NavParams,
    public formBuilder: FormBuilder
  ) {

    this.userLogin = formBuilder.group({
      femail: ['',Validators.compose([Validators.required,Validators.email])],
      fpassword:['',Validators.compose([Validators.required])]  //need to add regex
    });

    this.femail = this.userLogin.controls['femail'];
    this.fpassword = this.userLogin.controls['fpassword'];

  }//constructor ends here

  ionViewDidLoad() {
    console.log("ionViewDidLoad LoginPage");
  }

  login(){
    //to send data to server and verify credentials

    this.navCtrl.setRoot('HomePage');
    this.navCtrl.popToRoot();
  }

  signup(){
    this.navCtrl.push('SignupPage');
  }
}
