import requests

class Catalog:
    def __init__(self, api_key):
        self.headers = {
            'authority': 'kinopoiskapiunofficial.tech',
            'accept': 'application/json',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'x-api-key': api_key,
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