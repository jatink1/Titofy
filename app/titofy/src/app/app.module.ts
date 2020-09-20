import { BrowserModule } from "@angular/platform-browser";
import { ErrorHandler, NgModule } from "@angular/core";
import { IonicApp, IonicErrorHandler, IonicModule } from "ionic-angular";
import { SplashScreen } from "@ionic-native/splash-screen";
import { StatusBar } from "@ionic-native/status-bar";

import { MyApp } from "./app.component";
import { HomePage } from "../pages/home/home";
import { LoginPage } from "../pages/login/login";

import { Camera } from "@ionic-native/camera";
import { ServerUrlProvider } from "../providers/server-url/server-url";
import { HttpClientModule } from "@angular/common/http";
import { SwingModule } from "angular2-swing";
import { HttpModule } from "@angular/http";
import { FileTransfer } from "@ionic-native/file-transfer";
import { File } from '@ionic-native/file';

@NgModule({
  declarations: [MyApp, HomePage, LoginPage],
  imports: [
    BrowserModule,
    IonicModule.forRoot(MyApp, { mode: "ios" }),
    HttpClientModule,
    SwingModule,
    HttpModule
  ],
  bootstrap: [IonicApp],
  entryComponents: [MyApp, HomePage, LoginPage],
  providers: [
    StatusBar,
    SplashScreen,
    Camera,
    File,
    FileTransfer,
    { provide: ErrorHandler, useClass: IonicErrorHandler },
    ServerUrlProvider,
  ],
})
export class AppModule {}
