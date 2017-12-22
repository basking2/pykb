import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Location } from '@angular/common';
import { HttpUrlEncodingCodec } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-blob',
  templateUrl: './blob.component.html',
  styleUrls: ['./blob.component.css']
})
export class BlobComponent implements OnInit {

  token: string = localStorage.getItem('bearer')

  blobs: object = { 'blobs': [] }

  id: string

  constructor(
    private http: HttpClient,
    private location: Location,
    private route: ActivatedRoute,
  ) {
    this.id = route.snapshot.paramMap.get('id')
  }

  ngOnInit() {
    var auth = "bearer "+this.token;

    this.http.
      get('/api/blob', {'headers': {'Authorization': auth}}).
      subscribe(data => this.blobs = data )
  }

  onSubmit(event, text) {
    event.preventDefault()
    console.info(text)
  }

}
