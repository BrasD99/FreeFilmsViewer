import requests

class Catalog:
    def __init__(self, api_key):
        self.headers = {
            'x-api-key': api_key
        }
    
    def search_by_name(self, prompt, only_first=False):
        page_num = pages_count = 1
        films = []

        while page_num <= pages_count:
            params = {
                'keyword': prompt,
                'page': page_num,
            }
            response = requests.get(
                'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword',
                params=params,
                headers=self.headers
            )
            data = response.json()

            pages_count = data['pagesCount']

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