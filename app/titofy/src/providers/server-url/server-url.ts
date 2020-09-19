import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable()
export class ServerUrlProvider {

  api:string;

  constructor(public http: HttpClient) {
    console.log('Hello ServerUrlProvider Provider');
  }

  serverURL(){
    this.api = '';
  }

}
