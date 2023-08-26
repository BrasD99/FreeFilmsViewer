from common.catalog import Catalog
from common.handler import RequestHandler
from flask import Flask, render_template, request, redirect, url_for
import json

with open('config.json', 'r') as f:
    config = json.load(f)

api_key = config['api_key']
voidboost_uri = config['voidboost_uri']
catalog = Catalog(api_key)
handler = RequestHandler(voidboost_uri)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/search')
def search():
    query = request.args.get('query')
    films = catalog.search_by_name(query, only_first=True)
    if films:
        return render_template('search.html', films=films, query=query)
    return redirect(url_for('not_found'))

@app.route('/not_found') 
def not_found():
    return render_template('not_found.html')

@app.route('/watch/<int:film_id>')
def watch(film_id):
    film = catalog.search_by_id(film_id)
    if film:
        playlist_uri = handler.process(f'{voidboost_uri}/embed/{film_id}')
        if playlist_uri:
            return render_template('watch.html', playlist_uri=playlist_uri)

    return render_template('not_found.html')
    
app.run(port='8000')