import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Location } from '@angular/common';
import { HttpUrlEncodingCodec } from '@angular/common/http';

@Component({
  selector: 'app-blob',
  templateUrl: './blob.component.html',
  styleUrls: ['./blob.component.css']
})
export class BlobComponent implements OnInit {

  token: string = localStorage.getItem('bearer')

  blobs = { 'blobs': [ 'a', 'b' ] }

  constructor(
    private http: HttpClient,
    private location: Location,
  ) { }

  ngOnInit() {
    var auth = "bearer "+this.token

    this.http.get('/api/blob', {'headers': {'Authorization': auth}}).subscribe(data =>{})

  }

}
