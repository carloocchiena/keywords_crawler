issues:

DONE
modulo stop words non funziona regolarmente (risolto con nltk)
bites references before assignement: risolto con try \ catch
generazione link mancante: risolto per le pagine senza link esplicito che rimandano a root "/" con uno script addizionale
studiare celery-with-flask (troppo complesso e forse non necessario ora)
importato il multithreading su flask usando anche yield.
ottimizzato la funzione di urlcrawling con concurrent.futures
ottimizzato ritorno dei valori in iframe in page con ritorno immediato dei dati

IN PROGRESS:

sono riuscito a fare un run finalmente con multithreading (concurrent.futures). Vedo però che ritorna un valore non formattato, veramente brutto (check: how to flask stream in a web page) (oppure scaricare il csv)
ho anche rifattorizzato la funzione di url crawling. bestiale il risparmio, praticamente del 97%! da 5secondi per un run tipo su sito con 15 url a 5 millisecondi! W-O-W.

ora praticamente devo solo capire come ritornare quel valore in formato graficamente gradevole 

https://stackoverflow.com/questions/31948285/display-data-streamed-from-a-flask-view-as-it-updates 

capire bene il flusso (ora funziona tutto ma il primo run ritorna un errore)



DA FARE
provare impaginazione diversa 

ISSUES

velocità
eliminare var global

WARNING: il file process.py è sbagliato, copiando devo aver ranzato via delle parti, non so come mai, ma in ogni modo, scritto così il multithread chiama una funzione non esistente (update 19/11/2021)

AGGIORNAMENTO

su github real time

su /prod_main quando sono sicuro sia tutto in bolla magari una volta a settimana

poi comunque c'è da rifare un bel test globale di tutto


INPUT

super interessante questo thread, questo vuole fare esattamente la mia stessa cosa ma su 5 url alla volta (lol)
https://www.reddit.com/r/flask/comments/flrv0e/is_it_possible_to_use_multithreading_inside_of/

(contattato ma non mi ha risposto)

https://stackoverflow.com/questions/51613439/concurrent-futures-webscraping

tutti suggeriscono di usare questa strada https://blog.miguelgrinberg.com/post/using-celery-with-flask 

e anche valido sembra rake (anche se fa mostly la stessa mia cosa ma con una lib) https://github.com/csurfer/rake-nltk

anche con Yield non ci ho ancora capito un cazzo https://realpython.com/introduction-to-python-generators/

proviamo anche questa strada https://medium.com/analytics-vidhya/web-scraping-using-threading-in-python-flask-aad43edb44a8 

