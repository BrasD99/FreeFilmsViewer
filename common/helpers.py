import requests
from bs4 import BeautifulSoup
import re

def remove_ads(uri):
    response = requests.get(uri)
    soup = BeautifulSoup(response.content, 'html.parser')
    script_tags = soup.find_all('script')

    for script in script_tags:
        script_content = script.string
        if script_content and 'CDNplayerConfig' in script_content:
            modified_script = re.sub(r"'preroll': '[^']*'", "'preroll': ''", script_content)
            modified_script = re.sub(r"'default_quality': \(\(CDNquality !== null\) \? CDNquality : '[^']*'\)", "'default_quality': '1080p'", modified_script)
            script.string = modified_script
            break
    return str(soup)