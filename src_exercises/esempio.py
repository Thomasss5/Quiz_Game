# Programma semplice in Python

def saluta(nome):
    """Funzione che saluta una persona"""
    return f"Ciao, {nome}! Benvenuto!"

def somma(a, b):
    """Funzione che calcola la somma di due numeri"""
    return a + b

def media(numeri):
    """Funzione che calcola la media di una lista di numeri"""
    if len(numeri) == 0:
        return 0
    return sum(numeri) / len(numeri)

# Programma principale
if __name__ == "__main__": # pragma no cover
    # Test della funzione saluta
    print(saluta("Mario"))
    
    # Test della funzione somma
    risultato = somma(5, 3)
    print(f"5 + 3 = {risultato}")
    
    # Test della funzione media
    numeri = [10, 20, 30, 40, 50]
    media_numeri = media(numeri)
    print(f"La media di {numeri} è: {media_numeri}")
