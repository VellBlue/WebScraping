import tkinter as tk
from tkinter import messagebox, filedialog
import requests
from bs4 import BeautifulSoup

def scrape_website():
    url = entry.get()  # Ottieni l'URL dal campo di input
    try:
        response = requests.get(url)  # Effettua la richiesta GET alla pagina web
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')  # Analizza il contenuto HTML
            # Esempio di estrazione di dati, qui puoi personalizzare l'estrazione in base alle tue esigenze
            # Ad esempio, trovare tutti i tag 'a' (link) nella pagina:
            links = soup.find_all('a')
            # Stampa i link trovati
            for link in links:
                print(link.get('href'))
            messagebox.showinfo("Successo", "Web scraping completato!")
        else:
            messagebox.showerror("Errore", f"Errore {response.status_code} - Impossibile accedere all'URL")
    except requests.RequestException as e:
        messagebox.showerror("Errore di Connessione", f"Errore: {str(e)}")

def download_images():
    url = entry.get()
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Trova tutti i tag 'img' (immagini) nella pagina web
            images = soup.find_all('img')

            # Apri una finestra di dialogo per selezionare la cartella di destinazione per il download
            destination_folder = filedialog.askdirectory()
            if destination_folder:  # Se l'utente ha selezionato una cartella
                for index, image in enumerate(images):
                    image_url = image.get('src')
                    # Verifica se l'URL dell'immagine è assoluto o relativo e costruisci l'URL completo
                    if not image_url.startswith('http'):
                        image_url = url + image_url if not image_url.startswith('/') else url + '/' + image_url[1:]
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        # Scrivi l'immagine scaricata nella cartella selezionata nel formato 'image_index.jpg'
                        with open(f"{destination_folder}/image_{index+1}.jpg", 'wb') as f:
                            f.write(image_response.content)
                messagebox.showinfo("Successo", "Download delle immagini completato!")
        else:
            messagebox.showerror("Errore", f"Errore {response.status_code} - Impossibile accedere all'URL")
    except requests.RequestException as e:
        messagebox.showerror("Errore di Connessione", f"Errore: {str(e)}")

# Creazione dell'interfaccia grafica
root = tk.Tk()
root.title("Web Scraping Tool")
root.geometry("500x250")  # Imposta le dimensioni della finestra principale

# Imposta un font più grande per l'intera GUI
custom_font = ("Arial", 14)

label = tk.Label(root, text="Inserisci l'URL del sito web:", font=custom_font)
label.pack()

entry = tk.Entry(root, width=50, font=custom_font)
entry.pack()

scrape_button = tk.Button(root, text="Esegui Web Scraping", command=scrape_website, font=custom_font, width=20, height=2)
scrape_button.pack(pady=10)

download_button = tk.Button(root, text="Scarica Immagini", command=download_images, font=custom_font, width=20, height=2)
download_button.pack()

root.mainloop()
