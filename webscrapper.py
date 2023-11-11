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
        self.Url = Url
        self.Najlepsza_godzina = None
        Film.instancjie_classy.append(self)
        Film.filmy_do_wyboru.append(self.Nazwa)
    
    def __str__(self):
        return f'Film: {self.Nazwa}, Kino: {self.kino}, Godziny: {", ".join(self.Godziny)}'
    
    def dodajGodzine(self, godzina):
        self.Godziny.append(godzina)
    
    def __eq__(self, other):
        return self.Nazwa == other.Nazwa

    #funckjia sortowania po instancjiach klasy
    @classmethod
    def sprawdz_godziny(cls, wybrana_godzina, TYTUL):
        Pozadane_filmy = []
        for objekty in cls.instancjie_classy:
            if objekty.Nazwa == TYTUL:
                placeholder = 4000
                for H in objekty.Godziny:
                    h = hour_text_to_int(H, objekty)
                    roznica = abs(h - wybrana_godzina)
                    if roznica <= placeholder:
                        objekty.Najlepsza_godzina = H
                        placeholder = roznica
                Pozadane_filmy.append(objekty)
        return Pozadane_filmy

    #funkcjia pomocnicza
    @classmethod
    def TytulyDoWyboru(cls):
        for film in cls.instancjie_classy:
            print(film)

#funkcjia pomocnicza
def hour_text_to_int(hour, Film):
    try:
        cleand_hour = hour.replace(':', '')
        return int(cleand_hour)
    except ValueError:
        Film = None
        return int(999999)

def Web_Scrapper(url):
    #iniciajlizacjia selenium
    Lista_Filmow_nazwa_class = []
    chrome_options = Options()
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    titles = driver.title
    multikinocheck = url[-5:]
    #scrapping dla cinemacity
    if "Repertuar kina Cinema City" in titles:
        web_to_class(driver, url, czesc_z_lista =  "/html/body/section[3]/section/div[1]/section/div[2]", czesc_z_blokiem = 'movie-row', czesc_z_nazwa = 'qb-movie-name', czesc_z_godzinami = 'btn-primary')
        return 0
    #w wypadku scrappowania multikina
    elif multikinocheck in titles:
        
        return Lista_Filmow_nazwa_class
    #w wypadku scrappowania heliosa
    elif "Strona główna :" in titles:
        
        return Lista_Filmow_nazwa_class

#funkcjia scrapujaca strone. Zrobiona z zamyslem do wykorzystania w przypadku innym niz cinemacity. nie sprawdzona z innymi kinami
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
    
    print(f'Konice scrapowania {url}')
    
#niedodana opcjia do sprawdzania seansow w heliosie
def heliosscrape():
    print("helios")
    
#funkcjia ktora znajduje nazwe kina w linku                    
def read_from_back_until_slash(input_string):
    result = ""
    index = len(input_string) - 1

    while index >= 0 and input_string[index] != '//':
        result = input_string[index] + result
        index -= 1

    return result
#zbedna funckjia testujaca dzialanosc wpisywania danych do klas
def Test_klas(Lista_Filmow_nazwa_class):
    Film.TytulyDoWyboru()
    print(f"Dlugosc listy to {len(Lista_Filmow_nazwa_class)}")
    for i in Lista_Filmow_nazwa_class:
        print(f"Nazwa filmu: {i.Nazwa}")
        print(f"Nazwa kina: {i.kino}")
        for h in i.Godziny:
            print(f"godziny: {h}")

#zbedna funkcjia opowiedzialana za testownie podczas programowania 
def Test_sortu():
    print("amogus")
    Web_Scrapper('https://www.cinema-city.pl/kina/mokotow')
    Web_Scrapper('https://www.cinema-city.pl/kina/arkadia')
    Film.TytulyDoWyboru()
    sort_i_output(1900, 'CZAS KRWAWEGO KSIĘŻYCA')

#funkcjia ktora sortuje i wypisuje gdzie i kiedy najblizszy seans                
def sort_i_output(godzina, tytul):
    Wyniki = Film.sprawdz_godziny(hour_text_to_int(godzina, Film=None), tytul)
    for wynik in Wyniki:
        print(f"Nazwa filmu: {wynik.Nazwa}") 
        print(f"Nazwa kina: {read_from_back_until_slash(wynik.kino)}")
        print(f"Najlepsza Godzina: {wynik.Najlepsza_godzina}")
 
#funckja ktura daja uzytkonikowi moziliwosc sprawdzenia filmu            
def Uzywalana_wersjia(Urls):
    for url in Urls:
        Web_Scrapper(url)
    print(Film.filmy_do_wyboru)
    nazwa_od_in = input("Nazwa filmu: ")    
    godzina_od_in = input("podaj godzine(w formacie 19:00): ")
    sort_i_output(godzina_od_in, nazwa_od_in)

                

if __name__ == "__main__":
    #tu mozna dodac reszte kin cineamcity jesli jest taka potrzeba
    Urls = ['https://www.cinema-city.pl/kina/mokotow','https://www.cinema-city.pl/kina/arkadia']
    Uzywalana_wersjia(Urls)


    