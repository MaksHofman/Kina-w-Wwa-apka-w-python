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

    @classmethod
    def TytulyDoWyboru(cls):
        print(cls.filmy_do_wyboru)

def Web_Scrapper(url):
    Lista_Filmow_nazwa_class = []
    chrome_options = Options()
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    titles = driver.title
    multikinocheck = url[-5:]
    if "Repertuar kina Cinema City" in titles:
        cinemacityscrape(driver, url, Lista_Filmow_nazwa_class)
        return Lista_Filmow_nazwa_class
    elif multikinocheck in titles:
        multikinoscrape(driver, url, Lista_Filmow_nazwa_class)
        return Lista_Filmow_nazwa_class
    elif "Strona główna :" in titles:
        heliosscrape(driver, url, Lista_Filmow_nazwa_class)
        return Lista_Filmow_nazwa_class

def cinemacityscrape(driver, url, Lista_Filmow_nazwa_class):
    parent_elements = WebDriverWait(driver, 120).until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/section[3]/section/div[1]/section/div[2]")))
    parent2 = parent_elements
    Nazwa_kina = read_from_back_until_slash(url)
  
    #edge case z pierwszym filmem(ma inna nazwe)
    for edge_case in parent_elements:
        edge_movie_block = edge_case.find_element(By.XPATH, '/html/body/section[3]/section/div[1]/section/div[2]/div')
        movie_name = edge_movie_block.find_element(By.CLASS_NAME, 'qb-movie-name')
        godziny_wyswietlania = edge_movie_block.find_elements(By.CLASS_NAME, 'btn-primary')
        Objekt_Film = Film( Nazwa= movie_name.text, kino= Nazwa_kina)
        for godziny in godziny_wyswietlania:
            Objekt_Film.dodajGodzine(godziny.text)
        Lista_Filmow_nazwa_class.append(Objekt_Film)
   
    for info_filmowe in parent2:
        blok_z_filmem = info_filmowe.find_elements(By.CLASS_NAME, 'movie-row')
        for filmy in blok_z_filmem: 
            movie_name = filmy.find_element(By.CLASS_NAME, 'qb-movie-name')
            godziny_wyswietlania = filmy.find_elements(By.CLASS_NAME, 'btn-primary')
            Objekt_Film = Film( Nazwa= movie_name.text, kino= Nazwa_kina)
            for godziny in godziny_wyswietlania:
                Objekt_Film.dodajGodzine(godziny.text)
            Lista_Filmow_nazwa_class.append(Objekt_Film)
    
    #Test_klas(Lista_Filmow_nazwa_class=Lista_Filmow_nazwa_class)
    print('cinemacityscrape koniec')
  
#NIE dziala, Trzeba naprawc(jutro)    
def multikinoscrape(driver, url, Lista_Filmow_nazwa_class):
    parent_elements = WebDriverWait(driver, 120).until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[1]/main/div/div[1]/div[4]")))
    parent2 = parent_elements
    Nazwa_kina = read_from_back_until_slash(url)
    """
    #edge case z pierwszym filmem(ma inna nazwe)
    for edge_case in parent_elements:
        edge_movie_block = edge_case.find_element(By.CLASS_NAME, 'filmlist')
        movie_name = edge_movie_block.find_element(By.CLASS_NAME, 'filmlist__title')
        godziny_wyswietlania = edge_movie_block.find_elements(By.CLASS_NAME, 'filmlist__times')
        Objekt_Film = Film( Nazwa= movie_name.text, kino= Nazwa_kina)
        for godziny in godziny_wyswietlania:
            Objekt_Film.dodajGodzine(godziny.text)
        Lista_Filmow_nazwa_class.append(Objekt_Film)
   """
    for info_filmowe in parent2:
        blok_z_filmem = info_filmowe.find_elements(By.CLASS_NAME, 'filmlist')
        for filmy in blok_z_filmem: 
            movie_name = filmy.find_element(By.CLASS_NAME, 'filmlist__title')
            godziny_wyswietlania = filmy.find_elements(By.CLASS_NAME, 'filmlist__times')
            Objekt_Film = Film( Nazwa= movie_name.text, kino= Nazwa_kina)
            for godziny in godziny_wyswietlania:
                Objekt_Film.dodajGodzine(godziny.text)
            Lista_Filmow_nazwa_class.append(Objekt_Film)
    
    Test_klas(Lista_Filmow_nazwa_class=Lista_Filmow_nazwa_class)
    print('multikinoscrappe koniec')

def heliosscrape():
    print("helios")
                      
def read_from_back_until_slash(input_string):
    result = ""
    index = len(input_string) - 1

    while index >= 0 and input_string[index] != '/':
        result = input_string[index] + result
        index -= 1

    return result

def Test_klas(Lista_Filmow_nazwa_class):
    Film.TytulyDoWyboru()
    print(f"Dlugosc listy to {len(Lista_Filmow_nazwa_class)}")
    for i in Lista_Filmow_nazwa_class:
        print(f"Nazwa filmu: {i.Nazwa}")
        print(f"Nazwa kina: {i.kino}")
        for h in i.Godziny:
            print(f"godziny: {h}")
# Test
#Web_Scrapper('https://www.cinema-city.pl/kina/mokotow')
Web_Scrapper('https://multikino.pl/repertuar/warszawa-zlote-tarasy')
#Web_Scrapper('https://www.helios.pl/57,Warszawa/StronaGlowna/')