import subprocess
import shutil
import os
from bs4 import BeautifulSoup
from common.helpers import (
    prepare_config
)

client_config_path = 'client/src/app/config.ts'

config = prepare_config()
api_uri = config['api_uri']

with open(client_config_path, "r") as file:
    file_contents = file.read()

file_contents = file_contents.replace("API_URI_HOLDER", api_uri)

with open(client_config_path, "w") as file:
    file.write(file_contents)

install_command = "npm install"
build_command = "npm run build"
directory_to_run_in = "client"

subprocess.run(install_command, shell=True, check=True, cwd=directory_to_run_in)
subprocess.run(build_command, shell=True, check=True, cwd=directory_to_run_in)

favicon_file = 'client/src/favicon.png'
dist_dir = 'client/dist'
client_dir = 'client/dist/client'
static_dir = 'static'
scripts_dir = 'static/scripts'
styles_dir = 'static/styles'
templates_dir = 'templates'

if os.path.exists(static_dir):
    shutil.rmtree(static_dir)

os.makedirs(static_dir)
os.makedirs(scripts_dir)
os.makedirs(styles_dir)

if os.path.exists(templates_dir):
    shutil.rmtree(templates_dir)
os.makedirs(templates_dir)

for filename in os.listdir(client_dir):
    if filename.endswith(".css"):
        source_file_path = os.path.join(client_dir, filename)
        destination_file_path = os.path.join(styles_dir, filename)
        shutil.move(source_file_path, destination_file_path)
    elif filename.endswith(".js"):
        source_file_path = os.path.join(client_dir, filename)
        destination_file_path = os.path.join(scripts_dir, filename)
        shutil.move(source_file_path, destination_file_path)
    elif filename.endswith(".html"):
        source_file_path = os.path.join(client_dir, filename)
        destination_file_path = os.path.join(templates_dir, filename)
        shutil.move(source_file_path, destination_file_path)

shutil.rmtree(dist_dir)
shutil.copy(favicon_file, static_dir)

with open(f'{templates_dir}/index.html', "r", encoding="utf-8") as html_file:
    soup = BeautifulSoup(html_file, "html.parser")
    link_elements = soup.find_all("link", rel="stylesheet")
    for link in link_elements:
        href = link.get("href")
        link["href"] = f"{{{{ url_for('static', filename='styles/{href}') }}}}"

    favicon_element = soup.find("link", rel="icon")
    href = favicon_element.get("href")
    favicon_element["href"] = f"{{{{ url_for('static', filename='{href}') }}}}"
    
    script_elements = soup.find_all("script", src=True)
    for script in script_elements:
        src = script.get("src")
        script["src"] = f"{{{{ url_for('static', filename='scripts/{src}') }}}}"
    modified_html = str(soup)

with open(f'{templates_dir}/index.html', "w", encoding="utf-8") as html_file:
    html_file.write(modified_html)