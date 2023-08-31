import requests
import time

class Catalog:
    def __init__(self, api_key):
        self.headers = {
            'x-api-key': api_key
        }
    
    def search_by_name(self, prompt, only_first=False):
        page_num = pages_count = 1
        retry_limit = 3
        retry_delay = 1

        films = []

        while page_num <= pages_count:
            params = {
                'keyword': prompt,
                'page': page_num,
            }
            for i in range(retry_limit):
                response = requests.get(
                    'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword',
                    params=params,
                    headers=self.headers
                )

                if response.status_code == 200:
                    data = response.json()
                    break

                if i == retry_limit - 1:
                    raise Exception('Limit raised')

                print(f"Request failed with status code {response.status_code}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)

            pages_count = data['pagesCount']

            for film in data['films']:
                if film['rating'] == 'null':
                    film['rating'] = '-'
                if film['type'] == 'FILM':
                    film['_type'] = 'Фильм'
                elif film['type'] == 'TV_SERIES':
                    film['_type'] = 'Сериал'
                else:
                    film['_type'] = 'Неизвестно'
        
            films.extend([film for film in data['films']])

            if only_first:
                return films
            
            page_num += 1
        
        return films
    
    def search_by_id(self, film_id):
        try:
            response = requests.get(
                f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{film_id}',
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(e)
            return None