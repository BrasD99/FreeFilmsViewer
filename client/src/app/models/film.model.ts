export class Film {
    filmId: number;
    posterUrl: string;
    nameRu: string;
    year: string;
    filmLength: string;
    rating: number;
    _type: string;
  
    constructor(
        filmId: number, 
        posterUrl: string, 
        nameRu: string,
        year: string,
        filmLength: string,
        rating: number,
        _type: string) {
      this.filmId = filmId;
      this.posterUrl = posterUrl;
      this.nameRu = nameRu;
      this.year = year;
      this.filmLength = filmLength;
      this.rating = rating;
      this._type = _type;
    }
  }