import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AppConfig } from './config';
import { Film } from './models/film.model';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class FilmService {

  constructor(private httpClient: HttpClient) { }

  getFilms(query: string): Observable<{ status: boolean, films: Film[] }> {
    const url = `${AppConfig.api_uri}/search?q=` + query;

    return this.httpClient.get(url).pipe(
      map((response: any) => {
        return {
          status: response.status, // Include the status property
          films: response.films.map((filmData: any) => {
            return new Film(
              filmData.filmId,
              filmData.posterUrl,
              filmData.nameRu,
              filmData.year,
              filmData.filmLength,
              filmData.rating,
              filmData._type
            );
          })
        };
      })
    );
  }
}
