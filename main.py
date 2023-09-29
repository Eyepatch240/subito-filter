from scraper import *

query = str(input("Inserisci il nome dell'oggetto a cui sei interessato.\n"))

data_max = int(input("Di quanti giorni vuoi siano vecchi al massimo gli annunci? Se vuoi visualizzare solo quelli postati oggi, scrivi 0\n"))

results_query = scrape_items_subito(query, data_max)

avg_price = average(results_query)

filter_results(results_query, avg_price)

print(f'Il prezzo medio per {query} negli ultimi {data_max} giorni è {average(results_query)}€')

order_by_lowest(results_query)

price = int(input("Inserisci il prezzo massimo che deve avere l'annuncio\n"))

print('Ecco quello che ho trovato')

filter_by_price(results_query, price)

print_results(results_query)