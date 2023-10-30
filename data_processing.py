# Funzione che calcola il prezzo medio degli Oggetti 
def average(results_query):

    somma = 0
    i = 0

    for oggetto in results_query:
        somma += oggetto.Prezzo
        i += 1

    return int(somma / i)

# Funzione che filtra tutti gli oggetti fuori mercato, o non inerenti alla ricerca (annunci da 1 euro,
#  accessori ecc.)
def filter_results(results_query, median_price):
    results_query[:] = [oggetto for oggetto in results_query if oggetto.Prezzo > median_price/2 
                        and oggetto.Prezzo < median_price * 2]

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