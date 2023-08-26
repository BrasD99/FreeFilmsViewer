from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options

class RequestHandler:
    def __init__(self, init_uri):
        options = Options()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(init_uri)
        self.driver.execute_script("window.localStorage.setItem('pljsquality', '1080p');")
        self.playlist_uri = None

    def request_interceptor(self, request):
        print(request)
        if 'm3u8' in request.url and not self.playlist_uri:
            self.playlist_uri = request.url
    
    def process(self, uri):
        self.playlist_uri = None
        self.driver.request_interceptor = self.request_interceptor
        self.driver.get(uri)
        return self.playlist_uri
    
    def quit(self):
        self.driver.quit()