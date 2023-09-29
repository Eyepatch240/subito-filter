# SubitoFilter 🔍

SubitoFilter è un semplice script Python, che filtra i risultati di Subito.it, in base alla data di annuncio dei post, e al loro prezzo. Oltre a calcolarne il costo medio.

# Come funziona

Il programma ti chiederà di inserire  il nome dell'oggetto di tuo interesse e il numero massimo di giorni entro cui gli annunci devono essere considerati.
Il prezzo medio di tali annunci verrà calcolato e visualizzato. Infine, puoi filtrare gli annunci in base al prezzo massimo desiderato e visualizzarli.

# Requisiti

- Python 3.x
- BeautifulSoup4 (installabile tramite pip install beautifulsoup4)
- Requests (installabile tramite pip install requests)

# Utilizzo

- Esegui il file main.py
- Inserisci il nome dell'oggetto a cui sei interessato, ed il numero massimo di giorni entro cui gli annunci devono essere stati postati.
- A questo punto, vedrai stampato il prezzo medio, e potrai inserire il prezzo massimo desiderato
- Gli annunci verrano stampati in terminale

Esempio risultati:

Il prezzo medio per Oggetto Cercato negli ultimi 30 giorni è 350€
Ecco quello che ho trovato:
- Nome Annuncio 1 a 300€ postato il 10 gen, 2023 Link: [link_annuncio_1](link_annuncio_1)
- Nome Annuncio 2 a 340€ postato il 15 gen, 2023 Link: [link_annuncio_2](link_annuncio_2)
...

# Licenza

MIT

_Lo script è un work in progress_

