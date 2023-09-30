import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def Web_Scrapper(url):
    chrome_options = Options()
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    titles = driver.title
    multikinocheck = url[-5:]
    if "Repertuar kina Cinema City" in titles:
        cinemacityscrape()
    
    elif multikinocheck in titles:
        multikinoscrape()

    elif "Strona główna :" in titles:
        heliosscrape()
    
def cinemacityscrape():
    #"qb-movie-name" - classa filmow i biezesz w tagu h3 text i masz tytul filmu
    #class="btn btn-primary btn-lg" - classa czasu o ktorej to jest
    
    
    print('amogus')


def multikinoscrape():
    print("sus")

def heliosscrape():
    print("extemus")

# Test 
Web_Scrapper('https://www.cinema-city.pl/kina/mokotow')
Web_Scrapper('https://multikino.pl/repertuar/warszawa-zlote-tarasy')
Web_Scrapper('https://www.helios.pl/57,Warszawa/StronaGlowna/')