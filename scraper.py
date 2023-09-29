from bs4 import BeautifulSoup
import requests
import datetime
import re

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

        oggetti = html_dati.find_all(class_='items__item item-card item-card--small')

        return oggetti

# Funzione che estrae i dati dalle pagine
def scrape_items_subito(query, data_max):

    # Estrae i dati da Subito.it per la query specificata. Itera dalla 15ima pagina a salire, ritorna una lista di oggetti estratti dalle pagine.
    query = query.replace(' ', '+')

    current_page = 15
    for current_page in range(15, 0, -1):
        oggetti = scrape_html(current_page, query)

        for item in oggetti:

            # Vengono saltati gli oggetti venduti
            if item.find(class_='item-sold-badge'):
                continue
            
            data_oggetto = item.find('span', class_=re.compile(r'date'))
            
            # Il programma salta l'oggetto corrente se privo di Data
            if data_oggetto is None:
                continue
            
            data_oggetto = data_oggetto.text.strip()

            # Viene chiamata la funzione data_handling per ogni oggetto
            if data_handling(data_oggetto, data_max):
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

            link_oggetto = item.find('a', class_='SmallCard-module_link__hOkzY')
            if link_oggetto:
                link_oggetto = link_oggetto.get('href').strip()

            # Con i dati raccolti, si crea un'istanza Oggetto, che viene aggiunta alla lista
            oggetto = Oggetto(nome_oggetto, prezzo_oggetto, data_oggetto, link_oggetto)

            lista_oggetti.append(oggetto)
    return lista_oggetti

# Funzione che calcola il prezzo medio degli Oggetti 
def average(results_query):

    somma = 0
    i = 0

    for oggetto in lista_oggetti:
        somma += oggetto.Prezzo
        i+=1

    avg_price = somma / i

    return avg_price

# Funzione che filtra tutti gli oggetti fuori mercato, o non inerenti alla ricerca (annunci da 1 euro, accessori ecc.)
def filter_results(results_query, avg_price):
    results_query[:] = [oggetto for oggetto in results_query if oggetto.Prezzo > avg_price/2 and oggetto.Prezzo < avg_price * 2]

# Funzione che ordina gli oggetti per prezzo in ordine crescente
def order_by_lowest(results_query):

    length = len(results_query)
    for i in range(length):
        min = i
        for j in range(i+1, length):
            if results_query[min].Prezzo > results_query[j].Prezzo:
                min = j
        temp = results_query[min]
        results_query[min] = results_query[i]
        results_query[i] = temp

# Funzione che filtra gli oggetti in base al prezzo massimo inserito dall'utente
def filter_by_price(results_query, price):
    results_query[:] = [oggetto for oggetto in results_query if oggetto.Prezzo <= price]

# Funzione che gestisce la rilevanza a livello temporale degli annunci esaminati, chiamata da scrap_items_subito, ritorna Falso quando devono essere esaminati e raccolti, True quando devono essere saltati
def data_handling(data_oggetto, data_max):

    if 'Oggi' in data_oggetto:
        return False
    
    if 'Ieri' in data_oggetto and data_max >= 1:
        return False
    
    data_365 = 0
    
    # La data dell'oggetto viene pulita dell'orario dell'annuncio
    data_oggetto = data_oggetto.rstrip('0123456789: ')

    if data_max > 1:
        for mese in Mesi:
            if str(mese['nome']) in str(data_oggetto):
                data_oggetto = ''.join(filter(str.isdigit, data_oggetto))
                data_oggetto = int(data_oggetto)
                data_365 += mese['giorni'] + data_oggetto
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
            print(f'{oggetto.Nome} a {oggetto.Prezzo}€ postato {oggetto.Data} Link: {oggetto.Link}')
        else:
            print(f'{oggetto.Nome} a {oggetto.Prezzo}€ postato il {oggetto.Data} Link: {oggetto.Link}')