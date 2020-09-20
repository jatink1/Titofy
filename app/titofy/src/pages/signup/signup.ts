import { Component, ViewChild } from "@angular/core";
import { IonicPage, NavController, NavParams } from "ionic-angular";
import {
  FormGroup,
  FormBuilder,
  AbstractControl,
  Validators,
} from "@angular/forms";
import { Camera, CameraOptions } from "@ionic-native/camera";
import { HttpClient } from "@angular/common/http";
import { ServerUrlProvider } from "../../providers/server-url/server-url";

//to upload image as a file
import {
  FileTransfer,
  FileUploadOptions,
  FileTransferObject,
} from "@ionic-native/file-transfer";
import { File } from "@ionic-native/file";

@IonicPage()
@Component({
  selector: "page-signup",
  templateUrl: "signup.html",
})
export class SignupPage {
  userSignup: FormGroup;
  fsignupName: AbstractControl;
  fsignupEmail: AbstractControl;
  fsignupPassword: AbstractControl;
  fsignupGender: AbstractControl;
  fsignupdob: AbstractControl;
  fsignupAge: AbstractControl;
  fsignupProfileURL: AbstractControl;
  fpref: AbstractControl;

  aaa: any;
  myphoto: any;
  userDataWithPhoto: any;

  // form with slides
  @ViewChild("signupSlider") signupSlider;

  public slideOneForm: FormGroup;
  public slideTwoForm: FormGroup;

  public submitAttempt: boolean = false;
  // form with slides

  constructor(
    public navCtrl: NavController,
    public navParams: NavParams,
    public formBuilder: FormBuilder,
    public camera: Camera,
    public http: HttpClient,
    public serverURL: ServerUrlProvider,
    public transfer: FileTransfer,
    public file: File
  ) {
    // this.userSignup = formbuilder.group({
    //   fsignupName: ["", Validators.compose([Validators.required])],
    //   fsignupEmail: [
    //     "",
    //     Validators.compose([Validators.required, Validators.email]),
    //   ],
    //   fsignupPassword: ["", Validators.compose([Validators.required,Validators.maxLength(30),       Validators.minLength(8),])],
    //   fsignupGender: ["", Validators.compose([Validators.required])],
    //   fsignupdob: ["", Validators.compose([Validators.required])],
    //     fsignupAge: ["", Validators.compose([Validators.required, Validators.max(100),Validators.min(18),])],
    //   fsignupProfileURL: ["", Validators.compose([Validators.required])],
    //   fpref: ["", Validators.compose([Validators.required])],
    // });

   


    // slides 
    this.slideOneForm = formBuilder.group({
      fsignupName: ["", Validators.compose([Validators.required])],
      fsignupEmail: ["",Validators.compose([Validators.required, Validators.email])],
      fsignupPassword: ["", Validators.compose([Validators.required,Validators.maxLength(30),       Validators.minLength(8),])],
      fsignupGender: ["", Validators.compose([Validators.required])],
     
  });

  this.slideTwoForm = formBuilder.group({
    fsignupdob: ["", Validators.compose([Validators.required])],
        fsignupAge: ["", Validators.compose([Validators.required, Validators.max(100),Validators.min(18),])],
      fsignupProfileURL: ["", Validators.compose([Validators.required])],
      fpref: ["", Validators.compose([Validators.required])],
      
  });

  this.fsignupName = this.slideOneForm.controls["fsignupName"].value;
  this.fsignupPassword = this.slideOneForm.controls["fsignupPassword"].value;
  this.fsignupAge = this.slideTwoForm.controls["fsignupAge"].value;
  this.fsignupEmail = this.slideOneForm.controls["fsignupEmail"].value;
  this.fsignupGender = this.slideOneForm.controls["fsignupGender"].value;
  this.fsignupdob = this.slideTwoForm.controls["fsignupdob"].value;
  this.fsignupProfileURL = this.slideTwoForm.controls[
    "fsignupProfileURL"
  ].value;
  this.fpref = this.slideTwoForm.controls["fpref"].value;
  
  
  }//constructor ends here

  ionViewDidLoad() {
    console.log("ionViewDidLoad SignupPage");
  }

  // to upload photo
  async uploadPhoto() {
    const options: CameraOptions = {
      quality: 50,
      destinationType: this.camera.DestinationType.DATA_URL,
      sourceType: this.camera.PictureSourceType.PHOTOLIBRARY,
      saveToPhotoAlbum: false,
      allowEdit: true,
      targetWidth: 300,
      targetHeight: 300,
    };

    await this.camera.getPicture(options).then(
      (imageData) => {
        // imageData is either a base64 encoded string or a file URI
        // If it's base64 (DATA_URL):
        this.myphoto = "data:image/jpeg;base64," + imageData;

        // let blob: Blob = this.b64toBlob(this.myphoto);
        // this.aaa = blob;
      },
      (err) => {
        // Handle error
        console.log("Error in uploading picture: ", err);
      }
    );
  }

  b64toBlob(str) {
    // extract content type and base64 payload from original string
    var pos = str.indexOf(";base64,");
    var type = str.substring(5, pos);
    var s = str.substr(pos + 8);
    // decode base64
    var imageContent = this.dec(s);
    // create an ArrayBuffer and a view (as unsigned 8-bit)
    var buffer = new ArrayBuffer(imageContent.length);
    let view = new Uint8Array(buffer);

    // fill the view, using the decoded base64
    for (var n = 0; n < imageContent.length; n++) {
      view[n] = imageContent.charCodeAt(n);
    }

    // convert ArrayBuffer to Blob
    var blob = new Blob([buffer], { type: type });

    return blob;
  }
  dec(s) {
    var e = {},
      i, b = 0, c, x, l = 0, a,r = "", w = String.fromCharCode, L = s.length;
    var A = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    for (i = 0; i < 64; i++) {
      e[A.charAt(i)] = i;
    }
    for (x = 0; x < L; x++) {
      c = e[s.charAt(x)];
      b = (b << 6) + c;
      l += 6;
      while (l >= 8) {
        ((a = (b >>> (l -= 8)) & 0xff) || x < L - 2) && (r += w(a));
      }
    }
    return r;
  }


  // form with slides
  next() {
    this.signupSlider.slideNext();
  }

  prev() {
    this.signupSlider.slidePrev();
  }

  save() {
    this.submitAttempt = true;

        // if(!this.slideOneForm.valid){
        //     this.signupSlider.slideTo(0);
        // } 
        // else if(!this.slideTwoForm.valid){
        //     this.signupSlider.slideTo(1);
        // }
        // else {
            console.log("success!")
            console.log(this.slideOneForm.value);
            console.log(this.slideTwoForm.value);
       // }

       submitForm

  }

  //for submitting form
  async submitForm() {
    this.userDataWithPhoto = new FormData();

    this.userDataWithPhoto.append("display", this.myphoto);
    this.userDataWithPhoto.append("name",this.slideOneForm.controls["fsignupName"].value);
    this.userDataWithPhoto.append("email",this.slideOneForm.controls["fsignupEmail"].value);
    this.userDataWithPhoto.append("password",this.slideOneForm.controls["fsignupPassword"].value);
    this.userDataWithPhoto.append("gender",this.slideOneForm.controls["fsignupGender"].value);
    this.userDataWithPhoto.append("dob",this.slideTwoForm.controls["fsignupdob"].value);
    this.userDataWithPhoto.append("orient",this.slideTwoForm.controls["fsignupAge"].value);
    this.userDataWithPhoto.append("preferance",this.slideTwoForm.controls["fpref"].value );
    this.userDataWithPhoto.append("spotify",this.slideTwoForm.controls["fsignupProfileURL"].value);

    console.log(this.userDataWithPhoto);
    //now sending data to server
    await this.http
      .post("https://titofy.herokuapp.com" + "/signup", this.userDataWithPhoto)
      .subscribe((res) => {
        console.log(res);
      });

    this.navCtrl.pop();
  }
}
