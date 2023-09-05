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
    //const currentUrl = window.location.href;
    //const url = new URL(currentUrl);
    //this.searchQuery = url.searchParams.get("q");
  }

  handleSvgClick(searchText: string){
    this.backBtnClicked = false;
    this.searchQuery = searchText;
    //this.updateQuery();
  }

  onEnterPressed(searchText: string){
    this.backBtnClicked = false;
    this.searchQuery = searchText;
    //this.updateQuery();
  }

  updateQuery() {
    const currentUrl = new URL(window.location.href);

    if (currentUrl.searchParams.has('q')) {
      currentUrl.searchParams.set('q', this.searchQuery!);
    } else {
      currentUrl.searchParams.append('q', this.searchQuery!);
    }

    const updatedUrl = currentUrl.toString();

    window.history.pushState({}, '', updatedUrl);
  }
}
