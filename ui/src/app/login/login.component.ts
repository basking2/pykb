import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Location } from '@angular/common';
import { HttpUrlEncodingCodec } from '@angular/common/http';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  client_id: string = "";
  project_id: string = "";
  auth_uri: string = "";
  token_uri: string = "";
  anti_forgery_token: string = "test - fixme - replace this.";

  login_uri: string = "";

  constructor(
    private http: HttpClient,
    private location: Location,
  ) { }

  ngOnInit() {
    // Make the HTTP request:
    this.http.get('/oauth2/client').subscribe(data => {
      // Read the result field from the JSON response.
      this.client_id = data['client_id'];
      this.project_id = data['project_id'];
      this.auth_uri = data['auth_uri'];
      this.token_uri = data['token_uri'];

      this.login_uri = this.auth_uri +
        "?scope=profile email openid&client_id="+this.client_id +
        "&access_type=offline&include_granted_scopes=true&state="+this.anti_forgery_token +
        "&redirect_uri=http://localhost:8000/oauth2&response_type=code"
        ;


      this.http.get(
        data['auth_uri'],
        {
          "params": {
            'scope': 'profile email openid',
            'client_id': this.client_id,
            'access_type': 'offline',
            'include_granted_scopes': 'true',
            'state': this.anti_forgery_token,
            'redirect_uri': 'http://localhost:8000/login',
            'response_type': 'code',
          }
        }
      ).subscribe(data => {
      });
    });
  }

}
