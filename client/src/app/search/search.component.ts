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
    this.loadFilms();
  }

  onEnterPressed(searchText: string){
    this.searchQuery = searchText;
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
            titleClass: 'toastr-title',
            messageClass: 'toastr-message'
          });
        }
        this.spinner.hide();
        this.isSearched = true;
      },
      error: (error) => {
        console.error('Error fetching films:', error);
        this.toastr.error('При обработке запроса возникла ошибка', 'Ошибка', {
          positionClass: 'toast-top-center',
          titleClass: 'toastr-title',
          messageClass: 'toastr-message'
        });
        this.spinner.hide();
      }
    });
  }
}
