from common.catalog import Catalog
from common.helpers import remove_ads
from flask import Flask, render_template, request, redirect, url_for
import json

with open('config.json', 'r') as f:
    config = json.load(f)

api_key = config['api_key']
voidboost_uri = config['voidboost_uri']
catalog = Catalog(api_key)

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
    return remove_ads(f'{voidboost_uri}/embed/{film_id}')
    
#app.run(port='8000')