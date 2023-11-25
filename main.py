from scraper import *
from data_processing import *
import sys

print("Subito Filter")
def main():
    query = input("inserisci il nome dell'oggetto che stai cercando\n")
    data_max = int(input("Di quanti giorni vuoi siano vecchi al massimo gli annunci? se vuoi visualizzare solo quelli postati oggi, digita 0\n"))

    while True:
        if not scrape_items_subito(query, data_max):
            print(f"Nessun risultato trovato per gli ultimi {data_max} giorni, inserisci una data massima diversa, -1 per riavviare lo script, -2 per fermarlo.")
            data_max = int(input("Di quanti giorni vuoi siano vecchi al massimo gli annunci?\n"))
            if data_max == -1:
                main()
            elif data_max == -2:
                sys.exit(0)
        else:
            results_query = scrape_items_subito(query, data_max)
            break 

    order_by_lowest(results_query)

    filter_results(results_query, results_query[len(results_query)//2].Prezzo)

    print(f'Il prezzo medio per {query} negli ultimi {data_max} giorni è {average(results_query)}€')

    price = int(input("Inserisci il prezzo massimo che deve avere l'annuncio\n"))
    
    while True:
        results_test = results_query.copy()
        filter_by_price(results_test, price)
        if not results_test:
            choice = int(input(f"Nessun risultato trovato al prezzo selezionato, inserisci un prezzo piu' alto, -1 per riavviare lo script, -2 per fermarlo.\n"))
            if choice == -1:
                main()
            elif choice == -2:
                sys.exit(0)
            else:
                price = choice
        else:
            results_query = results_test
            break

    print('Ecco quello che ho trovato')
    print_results(results_query)

    choice = input("Vuoi fare una nuova ricerca? digita si, no altrimenti\n")
    if choice.lower() == "si":
        main()
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()