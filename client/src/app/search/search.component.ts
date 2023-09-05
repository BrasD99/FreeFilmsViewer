import { Component, Input, OnInit } from '@angular/core';
import { Film } from '../models/film.model';
import { FilmService } from '../films.service';
import { NgxSpinnerService } from 'ngx-spinner';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {
  @Input() searchQuery: string | null;
  isLoading: boolean = true;
  isSearched: boolean = false;
  films: Film[] = []

  constructor(
    private spinner: NgxSpinnerService,
    private toastr: ToastrService,
    private filmService: FilmService) {}

  ngOnInit() {
    this.loadFilms();
  }

  handleSvgClick(searchText: string){
    this.searchQuery = searchText;
    //this.updateQuery();
    this.loadFilms();
  }

  onEnterPressed(searchText: string){
    this.searchQuery = searchText;
    //this.updateQuery();
    this.loadFilms();
  }

  loadFilms() {
    this.spinner.show();
    this.filmService.getFilms(this.searchQuery!).subscribe({
      next: (response) => {
        if (response.status === true) {
          this.films = response.films;
        } else {
          this.toastr.warning('Лимит запросов исчерпан, возвращайтесь завтра!', 'Уведомление', {
            positionClass: 'toast-top-center',
          });
        }
        this.spinner.hide();
        this.isSearched = true;
      },
      error: (error) => {
        console.error('Error fetching films:', error);
        this.toastr.error('При обработке запроса возникла ошибка', 'Ошибка', {
          positionClass: 'toast-top-center',
        });
        this.spinner.hide();
      }
    });
  }

  updateQuery() {
    const currentUrl = new URL(window.location.href);
  
    // Check if the current URL already contains a query parameter named "q"
    if (currentUrl.searchParams.has('q')) {
      // If it exists, replace the existing value with the new value
      currentUrl.searchParams.set('q', this.searchQuery!);
    } else {
      // If it doesn't exist, add the new query parameter
      currentUrl.searchParams.append('q', this.searchQuery!);
    }
  
    // Get the updated URL with the modified query parameter
    const updatedUrl = currentUrl.toString();
  
    // Update the URL without triggering a page reload
    window.history.pushState({}, '', updatedUrl);
  }
}
