from bs4 import BeautifulSoup
import requests
import datetime
import re

STARTING_PAGE = 15

# Ottengo la data corrente in formato 365
data_attuale = datetime.date.today().timetuple().tm_yday

# Lista dei giorni corrispondenti su 365 all inizio di ogni mese
Mesi = [ {'nome': 'gen', 'giorni': 0},
    {'nome': 'feb', 'giorni': 31},
    {'nome': 'mar', 'giorni': 58},
    {'nome': 'apr', 'giorni': 90},
    {'nome': 'mag', 'giorni': 120},
    {'nome': 'giu', 'giorni': 151},
    {'nome': 'lug', 'giorni': 181},
    {'nome': 'ago', 'giorni': 212},
    {'nome': 'set', 'giorni': 243},
    {'nome': 'ott', 'giorni': 273},
    {'nome': 'nov', 'giorni': 304},
    {'nome': 'dic', 'giorni': 334}, ]

# Classe degli oggetti
class Oggetto:
    def __init__(self, nome, prezzo, data, link):
        self.Nome = nome
        self.Prezzo = prezzo
        self.Data = data
        self.Link = link

# Lista per contenere le istanze di oggetti
lista_oggetti = []

# Funziona per estrarre l'html dalla pagina, i corrisponde all'indice attuale, con cui si scende dalla pagina piu' "vecchia" a quella piu' nuova, query corrisponde all'oggetto ricercato dall'utente
def scrape_html(current_page, query):

        html_text = requests.get(f'https://www.subito.it/annunci-italia/vendita/usato/?q={query}&shp=true&qso=true&o={current_page}').text

        html_dati = BeautifulSoup(html_text, 'lxml')

        oggetti = html_dati.find_all(class_=re.compile(r'item-card'))

        return oggetti

# Funzione che estrae i dati dalle pagine
def scrape_items_subito(query, data_max):

    # Estrae i dati da Subito.it per la query specificata. Itera dalla 15ima pagina a salire, ritorna una lista di oggetti estratti dalle pagine.
    query = query.replace(' ', '+')

    current_page = STARTING_PAGE
    for current_page in range(STARTING_PAGE, 0, -1):
        oggetti = scrape_html(current_page, query)

        for item in oggetti:

            if item.find(class_='item-sold-badge'):
                continue
            
            data_oggetto = item.find('span', class_=re.compile(r'date'))
            
            # Per gli annunci privi di data, controlla che si tratti di un prodotto 'in vetrina' e se si, gli assegna 'Sponsorizzato'. 
            if data_oggetto is None:
                if item.find('div', class_=re.compile(r'TimeAndPlace-module_with-badge')):
                    data_oggetto = 'Sponsorizzato'
                else:
                    continue
            
            if not isinstance(data_oggetto, str):
                data_oggetto = data_oggetto.text.strip()

            # Viene chiamata la funzione data_handling per ogni oggetto, la quale gestisce gli oggetti in base alla data massima, inserita dall'utente. ritorna True se l'oggetto va skippato.
            if time_handling_subito(data_oggetto, data_max):
                continue

            nome_oggetto = item.find('h2').string.strip()

            prezzo_oggetto = item.find('p', class_=re.compile(r'price'))
            prezzo_oggetto = prezzo_oggetto.text.strip()
            # il prezzo viene estratto, e pulito da tutti i caratteri che circondano le cifre
            prezzo_oggetto = ''.join(filter(str.isdigit, prezzo_oggetto))
            try:
                prezzo_oggetto = int(prezzo_oggetto)
    
            except ValueError:
                continue

            link_oggetto = item.find('a', class_=re.compile(r'link'))
            if link_oggetto:
                link_oggetto = link_oggetto.get('href').strip()
                if any(item.Link == link_oggetto for item in lista_oggetti):
                    continue
            # Con i dati raccolti, si crea un'istanza Oggetto, che viene aggiunta alla lista
            oggetto = Oggetto(nome_oggetto, prezzo_oggetto, data_oggetto, link_oggetto)

            lista_oggetti.append(oggetto)
    return lista_oggetti

# Funzione che gestisce la rilevanza a livello temporale degli annunci esaminati, chiamata da scrap_items_subito, ritorna Falso quando devono essere esaminati e raccolti, True quando devono essere saltati
def time_handling_subito(data_oggetto, data_max):

    if 'Oggi' in data_oggetto or ('Ieri' in data_oggetto and data_max >= 1):
        return False

    if 'Sponsorizzato' in data_oggetto:
        return False 
    
    data_365 = 0
    
    # La data dell'oggetto viene pulita dell'orario dell'annuncio
    data_oggetto = data_oggetto.rstrip('0123456789: ')

    if data_max > 1:
        for mese in Mesi:
            if str(mese['nome']) in str(data_oggetto):
                data_oggetto = ''.join(filter(str.isdigit, data_oggetto))
                data_365 += mese['giorni'] + int(data_oggetto)
                break
    else:
        return True
    
    differenza = data_attuale - data_365

    if (-365 + data_max) < differenza < 0 or differenza > data_max:
        return True

# Stampa i risultati
def print_results(results_query):
    for oggetto in results_query:
        if 'Oggi' in oggetto.Data or 'Ieri' in oggetto.Data:
            print(f'{oggetto.Nome} a {oggetto.Prezzo}€, postato {oggetto.Data} \nLink: {oggetto.Link}')
        elif 'Sponsorizzato' in oggetto.Data:
            print(f'{oggetto.Nome} a {oggetto.Prezzo}€, in vetrina \nLink: {oggetto.Link}')
        else:
            print(f'{oggetto.Nome} a {oggetto.Prezzo}€, postato il {oggetto.Data} \nLink: {oggetto.Link}')