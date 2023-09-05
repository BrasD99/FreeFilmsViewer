import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  searchQuery: string | null;
  backBtnClicked: boolean = false;

  ngOnInit(): void {
    
  }

  handleSvgClick(searchText: string){
    this.backBtnClicked = false;
    this.searchQuery = searchText;
  }

  onEnterPressed(searchText: string){
    this.backBtnClicked = false;
    this.searchQuery = searchText;
  }
}
