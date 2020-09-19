import { Component } from "@angular/core";
import { IonicPage, NavController, NavParams } from "ionic-angular";
import {
  FormGroup,
  FormBuilder,
  AbstractControl,
  Validators,
} from "@angular/forms";
import { Camera, CameraOptions } from "@ionic-native/camera";
import { HttpClient } from "@angular/common/http";
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

  aaa: any;
  myphoto: any;
  userDataWithPhoto: any;

  constructor(
    public navCtrl: NavController,
    public navParams: NavParams,
    public formbuilder: FormBuilder,
    public camera: Camera,
    public http: HttpClient
  ) {
    this.userSignup = formbuilder.group({
      fsignupName: ["", Validators.compose([Validators.required])],
      fsignupEmail: [
        "",
        Validators.compose([Validators.required, Validators.email]),
      ],
      fsignupPassword: ["", Validators.compose([Validators.required])],
      fsignupGender: ["", Validators.compose([Validators.required])],
      fsignupdob: ["", Validators.compose([Validators.required])],
      fsignupAge: [
        "",
        Validators.compose([
          Validators.required,
          Validators.max(100),
          Validators.min(18),
        ]),
      ],
      fsignupProfileURL: ["", Validators.compose([Validators.required])],
    });
  }

  ionViewDidLoad() {
    console.log("ionViewDidLoad SignupPage");
  }

  // to upload photo
  uploadPhoto() {
    const options: CameraOptions = {
      quality: 50,
      destinationType: this.camera.DestinationType.DATA_URL,
      sourceType: this.camera.PictureSourceType.PHOTOLIBRARY,
      saveToPhotoAlbum: false,
      allowEdit: true,
      targetWidth: 300,
      targetHeight: 300,
    };

    this.camera.getPicture(options).then(
      (imageData) => {
        // imageData is either a base64 encoded string or a file URI
        // If it's base64 (DATA_URL):
        this.myphoto = "data:image/jpeg;base64," + imageData;
        let blob: Blob = this.b64toBlob(this.myphoto);
        this.aaa = blob;
      },
      (err) => {
        // Handle error
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
      i,
      b = 0,
      c,
      x,
      l = 0,
      a,
      r = "",
      w = String.fromCharCode,
      L = s.length;
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

  //for submitting form
  submitForm() {
    this.userDataWithPhoto = new FormData();

    this.userDataWithPhoto.append("photo", this.aaa, "image.jpeg");
    this.userDataWithPhoto.append(
      "userName",
      this.userSignup.controls["fsignupName"].value
    );
    this.userDataWithPhoto.append(
      "userEmail",
      this.userSignup.controls["fsignupEmail"].value
    );
    this.userDataWithPhoto.append(
      "userPassword",
      this.userSignup.controls["fsignupPassword"].value
    );
    this.userDataWithPhoto.append(
      "userGender",
      this.userSignup.controls["fsignupGender"].value
    );
    this.userDataWithPhoto.append(
      "userDOB",
      this.userSignup.controls["fsignupdob"].value
    );
    this.userDataWithPhoto.append(
      "userAge",
      this.userSignup.controls["fsignupAge"].value
    );
    this.userDataWithPhoto.append(
      "userSpotifyURL",
      this.userSignup.controls["fsignupProfileURL"].value
    );

    //now sending data to server
    this.http.post("url", this.userDataWithPhoto).subscribe((res) => {
      console.log(res);
    });
  }
}
