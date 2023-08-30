from common.catalog import Catalog
from common.helpers import (
    check_film_availability, 
    remove_ads, 
    make_proxy_request, 
    post, 
    get, 
    preprocess_thumbnails)
from flask import (
    Flask, 
    render_template, 
    request, 
    redirect, 
    url_for, 
    Response, 
    make_response)
import json
from urllib.parse import urlencode
import concurrent.futures
import os

with open('config.json', 'r') as f:
    config = json.load(f)

api_key = config['api_key']
voidboost_uri = config['voidboost_uri']

proxy_uri = os.getenv("proxy_uri")

if not proxy_uri:
    proxy_uri = config['proxy_uri']

catalog = Catalog(api_key)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/search')
def search():
    query = request.args.get('query')

    films = catalog.search_by_name(query)
    films = [film for i, film in enumerate(films) if film['filmId'] \
             not in {x['filmId'] for x in films[:i]}]
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(check_film_availability, films, [voidboost_uri] * len(films))
    films = [film for film in results if film is not None]

    if films:
        return render_template('search.html', films=films, query=query)
    return redirect(url_for('not_found'))

@app.route('/not_found') 
def not_found():
    return render_template('not_found.html')

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    response, headers = make_proxy_request(url, proxy_uri)

    if headers:
        return make_response(response, headers)
    
    response = Response(response)
    return response

@app.route('/movie/<slug>/iframe')
def movie_iframe(slug):
    uri = f'{voidboost_uri}/movie/{slug}/iframe'
    query_args = {
        's': request.args.get('s'),
        'e': request.args.get('e'),
        'h': request.args.get('h')
    }
    filtered_args = {key: value for key, value in query_args.items() \
                      if value is not None}
    if filtered_args:
        query = urlencode(query_args)
        uri += f'?{query}'

    return remove_ads(uri, proxy_uri)

@app.route('/serial/<slug>/iframe')
def serial_iframe(slug):
    uri = f'{voidboost_uri}/serial/{slug}/iframe'
    query_args = {
        's': request.args.get('s'),
        'e': request.args.get('e'),
        'h': request.args.get('h')
    }
    filtered_args = {key: value for key, value in query_args.items() \
                      if value is not None}
    if filtered_args:
        query = urlencode(query_args)
        uri += f'?{query}'
    
    return remove_ads(uri, proxy_uri)

@app.route('/serial/data', methods=['POST'])
def serial_data():
    data = request.get_data().decode('utf-8')
    data = dict(arg.split('=') for arg in data.split('&'))
    return post(f'{voidboost_uri}/serial/data', data)

@app.route('/embed/<path:video_info>')
def embed_video(video_info):
    uri = f'{voidboost_uri}/embed/{video_info}'
    query_args = {
        'autoplay': request.args.get('autoplay'),
        'start': request.args.get('start'),
        's': request.args.get('s'),
        'e': request.args.get('e'),
        'h': request.args.get('h')
    }
    filtered_args = {key: value for key, value in query_args.items() \
                      if value is not None}
    if filtered_args:
        query = urlencode(query_args)
        uri += f'?{query}'

    return remove_ads(uri, proxy_uri)

@app.route('/embed/<int:film_id>')
def embed(film_id):
    query_args = {
        'autoplay': request.args.get('autoplay'),
        'start': request.args.get('start'),
        's': request.args.get('s'),
        'e': request.args.get('e'),
        'h': request.args.get('h')
    }
    filtered_args = {key: value for key, value in query_args.items() \
                      if value is not None}

    target_url = url_for(f'watch', film_id=film_id, **filtered_args)

    return redirect(target_url)

@app.route('/watch/<int:film_id>')
def watch(film_id):
    uri = f'{voidboost_uri}/embed/{film_id}'
    query_args = {
        'autoplay': request.args.get('autoplay'),
        'start': request.args.get('start'),
        's': request.args.get('s'),
        'e': request.args.get('e'),
        'h': request.args.get('h')
    }
    filtered_args = {key: value for key, value in query_args.items() \
                      if value is not None}
    
    if filtered_args:
        query = urlencode(query_args)
        uri += f'?{query}'

    return remove_ads(uri, proxy_uri)

@app.route('/app/views/images/<path:image_path>')
def serve_image(image_path):
    uri = f'{voidboost_uri}/app/views/images/{image_path}'
    return get(uri)

@app.route('/s')
def s():
    uri = f'{voidboost_uri}/s'

    query_args = {
        'd': request.args.get('d'),
        '_': request.args.get('_')
    }
    filtered_args = {key: value for key, value in query_args.items() \
                      if value is not None}
    
    if filtered_args:
        query = urlencode(query_args)
        uri += f'?{query}'

    return get(uri)

@app.route('/thumbnails/<slug>/<int:timestamp>')
def generate_thumbnail(slug, timestamp):
    uri = f'{voidboost_uri}/thumbnails/{slug}/{timestamp}'
    return preprocess_thumbnails(uri, proxy_uri)

app.run(port='8000')