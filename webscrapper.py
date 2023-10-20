import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class Film():
    filmy_do_wyboru = []
    instancjie_classy = []
    
    def __init__(self, Nazwa, kino, Url):
        self.Nazwa = Nazwa
        self.kino = kino
        self.Godziny = []
        Film.filmy_do_wyboru.append(Nazwa + '.' + kino)
        self.Url = Url
        Film.instancjie_classy.append(self)
    
    def dodajGodzine(self, godzina):
        self.Godziny.append(godzina)

    @classmethod
    def sprawdz_godziny(cls, wybrana_godzina):
        place_holder = [4000, 'Nazwa poszczegulnej instacji']
        for Film in cls.instancjie_classy:
            for H in Film.Godziny:
                h = hour_text_to_int(H)
                roznca = abs(h - wybrana_godzina)
                if roznca == 0:
                    return Film
                elif h < place_holder[0]:
                    place_holder[0] = h
                    place_holder[1] = Film
                elif roznca == place_holder[0]: #trzeba pomyslec o tym
                    place_holder.append(Film)

            return place_holder[1:]
    #przetestuj czy dziala
    
    @classmethod
    def TytulyDoWyboru(cls):
        print(cls.filmy_do_wyboru)

def hour_text_to_int(hour):
    cleand_hour = hour.replace('.', '')
    return int(cleand_hour)
    

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
        web_to_class(driver, url, czesc_z_lista =  "/html/body/section[3]/section/div[1]/section/div[2]", czesc_z_blokiem = 'movie-row', czesc_z_nazwa = 'qb-movie-name', czesc_z_godzinami = 'btn-primary')
        return 0
    elif multikinocheck in titles:
        
        return Lista_Filmow_nazwa_class
    elif "Strona główna :" in titles:
        
        return Lista_Filmow_nazwa_class

def web_to_class(driver, url, czesc_z_lista, czesc_z_blokiem, czesc_z_nazwa, czesc_z_godzinami):
    parent_elements = WebDriverWait(driver, 120).until(EC.presence_of_all_elements_located((By.XPATH, czesc_z_lista)))
    parent2 = parent_elements
    Nazwa_kina = read_from_back_until_slash(url)

    for info_filmowe in parent2:
        blok_z_filmem = info_filmowe.find_elements(By.CLASS_NAME, czesc_z_blokiem)
        for filmy in blok_z_filmem: 
            movie_name = filmy.find_element(By.CLASS_NAME, czesc_z_nazwa)
            godziny_wyswietlania = filmy.find_elements(By.CLASS_NAME, czesc_z_godzinami)
            Objekt_Film = Film( Nazwa= movie_name.text, kino= Nazwa_kina, Url=url)
            for godziny in godziny_wyswietlania:
                Objekt_Film.dodajGodzine(godziny.text)
    
    Test_klas(Lista_Filmow_nazwa_class=Lista_Filmow_nazwa_class)
    print(f'Konice scrapowania {url}')


def heliosscrape():
    print("helios")
                      
def read_from_back_until_slash(input_string):
    result = ""
    index = len(input_string) - 1

    while index >= 0 and input_string[index] != '//':
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
Web_Scrapper('https://www.cinema-city.pl/kina/mokotow')
Web_Scrapper('https://multikino.pl/repertuar/warszawa-zlote-tarasy')
#Web_Scrapper('https://www.helios.pl/57,Warszawa/StronaGlowna/')
# cinema czesc_z_lista =  "/html/body/section[3]/section/div[1]/section/div[2]", czesc_z_blokiem = 'movie-row', czesc_z_nazwa = 'qb-movie-name', czesc_z_godzinami = 'btn-primary'



    