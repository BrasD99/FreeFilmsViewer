import { TestBed } from '@angular/core/testing';

import { FilmService } from './films.service';

describe('FilmService', () => {
  let service: FilmService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FilmService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
