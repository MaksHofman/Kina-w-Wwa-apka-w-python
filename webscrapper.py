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
    parent_elements = WebDriverWait(driver, 120).until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/section[3]/section/div[1]/section/div[2]")))
    
    #edge case z pierwszym filmem(ma inna nazwe) - DZIALA
    for edge_case in parent_elements:
        edge_movie_block = edge_case.find_element(By.XPATH, '/html/body/section[3]/section/div[1]/section/div[2]/div')
        movie_name = edge_movie_block.find_element(By.CLASS_NAME, 'qb-movie-name')
        godziny_wyswietlania = edge_movie_block.find_elements(By.CLASS_NAME, 'btn-primary')
            #test
        print(movie_name.text)
        for godziny in godziny_wyswietlania:
            print(godziny.text)
        print("--------------")
    
    #NIEDZIALA NW DLACZEGO
    for info_filmowe in parent_elements:
        blok_z_filmem = info_filmowe.find_elements(By.CLASS_NAME, 'row qb-movie')
        for filmy in blok_z_filmem:
            movie_name = filmy.find_element(By.CLASS_NAME, 'qb-movie-name')
            godziny_wyswietlania = filmy.find_elements(By.CLASS_NAME, 'btn-primary')
            #test
            print(movie_name.text)
            for godziny in godziny_wyswietlania:
                print(godziny.text)
            print("--------------")
    
    #for ti in parent_elements:
        #print(ti.text)
    print('cinemacityscrape koniec')


def multikinoscrape():
    print("sus")

def heliosscrape():
    print("extemus")

# Test 
Web_Scrapper('https://www.cinema-city.pl/kina/mokotow/1070#/buy-tickets-by-cinema?in-cinema=1070&at=2023-10-04&view-mode=list')
#Web_Scrapper('https://www.cinema-city.pl/kina/mokotow')
#Web_Scrapper('https://multikino.pl/repertuar/warszawa-zlote-tarasy')
#Web_Scrapper('https://www.helios.pl/57,Warszawa/StronaGlowna/')

