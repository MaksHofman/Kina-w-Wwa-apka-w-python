import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class Film():
    filmy_do_wyboru = []
    
    def __init__(self, Nazwa, kino):
        self.Nazwa = Nazwa
        self.kino = kino
        self.Godziny = []
        Film.filmy_do_wyboru.append(Nazwa + '.' + kino)

    def dodajGodzine(self, godzina):
        self.Godziny.append(godzina)



    def TytulyDoWyboru(cls):
        print(Film.filmy_do_wyboru)


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
        cinemacityscrape(driver)
    
    elif multikinocheck in titles:
        multikinoscrape(driver)

    elif "Strona główna :" in titles:
        heliosscrape(driver)
  
def webDataToClass(kino, film, godziny):
    print("hello")    
    
    
def cinemacityscrape(driver):
    #"qb-movie-name" - classa filmow i biezesz w tagu h3 text i masz tytul filmu
    #class="btn btn-primary btn-lg" - classa czasu o ktorej to jest
    parent_elements = WebDriverWait(driver, 120).until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/section[3]/section/div[1]/section/div[2]")))
    #movie_element = parent_elements.find_elements(By.CLASS_NAME, "qb-movie-name")
    #time_elements = parent_elements.find_elements(By.CLASS_NAME, "btn btn-primary btn-lg")# niedziala chyba
    #print(movie_element.text)
    #print(time_elements)
    for element in parent_elements:
        movie_name = element.find_elements(By.CLASS_NAME, 'qb-movie-name')#problem z class names
        for godziny in movie_name:
            hours = godziny.find_elements(By.CLASS_NAME, 'btn-primary')#sa zle bo nie sa w tym samym divie chyba
        for movies in movie_name:
            print(movies.text)
            for god in hours:
                print(god.text)
            print("--------------")
    
    #for ti in parent_elements:
        #print(ti.text)
    print('cinemacityscrape koniec')


def multikinoscrape():
    print("sus")

def heliosscrape():
    print("extemus")

# Test 
Web_Scrapper('https://www.cinema-city.pl/kina/mokotow')
#Web_Scrapper('https://multikino.pl/repertuar/warszawa-zlote-tarasy')
#Web_Scrapper('https://www.helios.pl/57,Warszawa/StronaGlowna/')

