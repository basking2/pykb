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

  // Report any errors regarding login operations.
  error: string = undefined;

  // Built from a call to /oauth2/client.
  login_uri: string = "";

  constructor(
    private http: HttpClient,
    private location: Location,
  ) { }

  ngOnInit() {

    // If there is a code parameter, the user is trying to validate a token.
    if (location.search.indexOf('code=') >= 0) {
      this.http.get('/oauth2/validate' + location.search).subscribe(data =>{
        if (data['token']) {
          localStorage.setItem('bearer', data['token'])
        }
        else {
          this.error = data['error']
        }
        this.location.go('/login')
      })
    }
    else {
      // Make the HTTP request:
      this.http.get('/oauth2/client').subscribe(data => {

        // Read the result field from the JSON response.
        this.login_uri = data['auth_uri'] +
          "?scope=profile email openid&client_id="+data['client_id'] +
          "&access_type=offline&include_granted_scopes=true&state="+data['state'] +
          "&redirect_uri=http://localhost:8000/login&response_type=code"
          ;
      });
    }
  }
}
