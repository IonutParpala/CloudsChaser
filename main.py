import requests
from bs4 import BeautifulSoup
import csv
import matplotlib.pyplot as plt
import time
import random
from clase import NarghileaLounge

def extrage_date_ialoc():
    url = "https://ialoc.ro/restaurante-bucuresti?tip=narghilea"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    time.sleep(2) 
    
    raspuns = requests.get(url, headers=headers) 
    
    if raspuns.status_code != 200:
        print(f"Eroare la conectare. Cod status: {raspuns.status_code}")
        return []

    soup = BeautifulSoup(raspuns.content, 'html.parser')
    localuri_gasite = []

    containere_localuri = soup.find_all('div', class_='list-item-details') 

    for container in containere_localuri:
        try:
            nume = container.find('span', class_='title').text.strip()
            
            adresa_element = container.find('address', class_='item-address')
            adresa = adresa_element.text.strip() if adresa_element else "Adresă necunoscută"
            
            nota_element = container.find('span', class_='rating-numbers')
            if nota_element:
                text_nota = nota_element.text.strip()
                nota_curata = text_nota.split('/')[0].replace('(', '').replace(',', '.').strip()
                nota = float(nota_curata)
            else:
                nota = 0.0

            local_nou = NarghileaLounge(nume, adresa, nota)
            localuri_gasite.append(local_nou)
            
        except AttributeError:
            continue

    return localuri_gasite

def salveaza_in_csv(lista_localuri):
    with open('narghilea_top.csv', 'w', newline='', encoding='utf-8') as fisier:
        writer = csv.writer(fisier)
        writer.writerow(['Nume Local', 'Adresa', 'Nota'])
        for local in lista_localuri:
            writer.writerow([local.nume, local.adresa, local.nota])
    print(f"Am salvat pentru tine {len(lista_localuri)} localuri direct în narghilea_top.csv!")

def analizeaza_si_deseneaza(lista_localuri):
    if not lista_localuri:
        return

    top_localuri = list(filter(lambda local: local.nota > 4.5, lista_localuri))
    
    if not top_localuri:
        print("Nu am găsit localuri cu nota peste 4.5.")
        return

    nume_localuri = list(map(lambda local: local.nume[:15] + '...', top_localuri)) 
    note_localuri = list(map(lambda local: local.nota, top_localuri))
    
    print("\nTop Localuri (Notă > 4.5):")
    for local in top_localuri:
        print(local)
        
    plt.figure(figsize=(10, 6)) 
    plt.bar(nume_localuri, note_localuri, color='#e74c3c')
    plt.title('CloudsChaser: Top Localuri Narghilea București')
    plt.xlabel('Nume Local')
    plt.ylabel('Nota (din 5)')
    plt.ylim(0, 5.5)
    plt.xticks(rotation=45, ha='right') 
    plt.tight_layout() 
    plt.savefig("top_narghilea.png")
    print(f"\nAi un top din partea noastra 'top_narghilea.png'!")

    recomandare = random.choice(top_localuri)
    print(f"\nNu te-ai decis singur? Iti recomanda un alt pasionat ca tine! Încearcă la {recomandare.nume}!")

if __name__ == "__main__":
    print("CloudsChaser...\n")
    datele_noastre = extrage_date_ialoc()
    if datele_noastre:
        salveaza_in_csv(datele_noastre)
        analizeaza_si_deseneaza(datele_noastre)
    else:
        print("Nu am găsit niciun local. Ceva a mers greșit la conectare sau procesare.")