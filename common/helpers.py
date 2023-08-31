import requests
from bs4 import BeautifulSoup
import re
from enum import Enum
from common.decryptor import decrypt, encrypt
from urllib.parse import quote

class STATES(Enum):
    AVAILABLE = 0
    NOT_AVAILABLE = 1
    SERVER_ERROR = 2

def check_film_availability(film, voidboost_uri):
    state = check_availavility(f'{voidboost_uri}/embed/{film["filmId"]}')
    return film if state == STATES.AVAILABLE else None

def check_availavility(uri):
    response = requests.get(uri)
    if response.status_code == 200:
        return STATES.AVAILABLE
    if response.status_code == 404:
        return STATES.NOT_AVAILABLE
    return STATES.SERVER_ERROR

def make_proxy_request(uri, proxy_uri):
    response = requests.get(uri)
    headers = dict(response.headers)
    if 'm3u8' in uri:
        uri = response.url
        modified_file = ""
        for line in response.text.split("\n"):
            if line.endswith(".ts"):
                configured_uri = uri.replace('manifest.m3u8', '')
                full_proxy = f'{proxy_uri}{configured_uri}'
                ts_name = line.split(':')[2]
                modified_line = full_proxy + ts_name
                modified_file += modified_line + "\n"
            else:
                modified_file += line + "\n"

        return modified_file, headers
    return response.content, headers

def post(uri, data):
    response = requests.post(uri, data)
    return response.content

def get(uri):
    response = requests.get(uri)
    return response.content

def preprocess_thumbnails(uri, proxy_uri):
    response = requests.get(uri)
    output = ''
    pattern = re.compile(r'^(https?|ftp)://[^\s/$.?#].[^\s]*$')
    for line in response.text.split("\n"):
        if re.match(pattern, line):
            output += f'{proxy_uri}{line}\n'
        else:
            output += f'{line}\n'
    return output

def remove_ads(uri, proxy_uri):
    response = requests.get(uri)
    soup = BeautifulSoup(response.content, 'html.parser')

    favicon_link = soup.new_tag('link', rel='shortcut icon', href='/static/favicon.png')
    soup.head.append(favicon_link)

    title_tag = soup.find('title')
    title_tag.string = 'Видеоплеер'

    css_link = '<link rel="stylesheet" href="/static/styles/watch.css">'
    js_link = '<script src="/static/scripts/watch.js"></script>'

    # Injecting css
    css_soup = BeautifulSoup(css_link, 'html.parser')
    soup.head.append(css_soup.link)

    # Injecting js
    body_tag = soup.body
    js_soup = BeautifulSoup(js_link, 'html.parser')
    body_tag.append(js_soup.script)

    # Modifying style
    #style_tag = soup.head.find('style')
    #style_tag.string = style_tag.string.replace('top: 7px !important;', 'top: 40px !important;')

    # Modifying body's style
    body_tag = soup.body
    body_tag['style'] = 'background-color: black;'

    # Injecting button
    #button_html = '''
    #    <button id="back_btn" class="custom-btn btn-design">Вернуться на страницу поиска</button>
    #'''
    #button_soup = BeautifulSoup(button_html, 'html.parser')
    #body_tag = soup.body
    #body_tag.insert(0, button_soup.button)

    script_tags = soup.find_all('script')

    for script in script_tags:
        script_content = script.string
        if script_content and 'CDNplayerConfig' in script_content:
            modified_script = re.sub(r"'preroll': '[^']*'", "'preroll': ''", script_content)
            match = re.search(r"'file':\s*'([^']*)'", modified_script)
            if match:
                data_value = match.group(1)
                decrypted, prefix = decrypt(data_value)
                modified = modify_for_proxy(decrypted, proxy_uri)
                encrypted = encrypt(modified, prefix)
                modified_script = re.sub(r"'file': '[^']*'", f"'file': '{encrypted}'", modified_script)
            script.string = modified_script
            break
    return str(soup)

def modify_for_proxy(data, url):
    inputs = data.split(',')
    final_string = ''
    for i, input in enumerate(inputs):
        or_array = input.split(' or ')
        for j, or_item in enumerate(or_array):
            match = re.search(r'\[([^\]]+)\]', or_item)
            quality = None
            if match:
                quality = match.group(1)
                or_item = or_item.replace(quality, '').replace('[]', '')
            encoded_uri = quote(or_item, safe=':/#')
            if quality:
                temp = f'[{quality}]' + url + str(encoded_uri)
            else:
                temp = url + encoded_uri
            
            if j != len(or_array) - 1:
                    temp += ' or '
            elif i != len(inputs) - 1:
                temp += ','
            final_string += temp
    return final_string

def get_redirect_uri(uri):
    response = requests.get(uri)
    return response.url