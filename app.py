import concurrent.futures

from flask import Flask, make_response, redirect, render_template, request, url_for, jsonify

from common.catalog import Catalog
from common.helpers import (
    check_film_availability,
    get,
    make_proxy_request,
    map_uri_args,
    post,
    prepare_config,
    preprocess_thumbnails,
    remove_ads,
)

config = prepare_config()
api_key = config['api_key']
voidboost_uri = config['voidboost_uri']
proxy_uri = config['proxy_uri']
retry_limit = config['retry_limit']
retry_delay = config['retry_delay']

catalog = Catalog(api_key)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/api/search', methods=['GET'])
def api_search():
    query = request.args.get('q')
    try:
        films = catalog.search_by_name(query, retry_limit, retry_delay, only_first=True)

        films = [film for i, film in enumerate(films) if film['filmId'] \
                not in {x['filmId'] for x in films[:i]}]
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(check_film_availability, films, [voidboost_uri] * len(films))
        films = [film for film in results if film is not None]

        response_data = {
            "status": True,
            "films": films
        }

    except Exception as e:
        print(f'An error occured: {e}')
        response_data = {
            "status": False,
            "films": []
        }
    
    response = jsonify(response_data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    response, headers = make_proxy_request(url, proxy_uri)
    return make_response(response, headers)

@app.route('/movie/<slug>/iframe')
def movie_iframe(slug):
    uri = map_uri_args(f'{voidboost_uri}/movie/{slug}/iframe', request.args)
    return remove_ads(uri, proxy_uri)

@app.route('/serial/<slug>/iframe')
def serial_iframe(slug):
    uri = map_uri_args(f'{voidboost_uri}/serial/{slug}/iframe', request.args)
    return remove_ads(uri, proxy_uri)

@app.route('/serial/data', methods=['POST'])
def serial_data():
    data = request.get_data().decode('utf-8')
    data = dict(arg.split('=') for arg in data.split('&'))
    return post(f'{voidboost_uri}/serial/data', data)

@app.route('/embed/<path:video_info>')
def embed_video(video_info):
    uri = map_uri_args(f'{voidboost_uri}/embed/{video_info}', request.args)
    return remove_ads(uri, proxy_uri)

@app.route('/embed/<int:film_id>')
def embed(film_id):
    args = request.args.to_dict()

    target_url = url_for('watch', film_id=film_id, **args)

    return redirect(target_url)

@app.route('/watch/<int:film_id>')
def watch(film_id):
    uri = map_uri_args(f'{voidboost_uri}/embed/{film_id}', request.args)
    return remove_ads(uri, proxy_uri)

@app.route('/app/views/images/<path:image_path>')
def serve_image(image_path):
    uri = f'{voidboost_uri}/app/views/images/{image_path}'
    return get(uri)

@app.route('/s')
def s():
    uri = map_uri_args(f'{voidboost_uri}/s', request.args)
    return get(uri)

@app.route('/thumbnails/<slug>/<int:timestamp>')
def generate_thumbnail(slug, timestamp):
    uri = f'{voidboost_uri}/thumbnails/{slug}/{timestamp}'
    return preprocess_thumbnails(uri, proxy_uri)

#app.run(port='8000')