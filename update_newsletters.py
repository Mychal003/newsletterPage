import os
import json
import re
import time
import traceback
import platform

# Sprawdź, czy uruchamiamy w WSL
is_wsl = "microsoft" in platform.uname().release.lower()
print(f"Uruchamianie w WSL: {is_wsl}")

# Dostosuj ścieżki w zależności od środowiska
if is_wsl:
    # Ścieżka dla WSL - zakładając, że pracujemy w tym samym folderze
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    PDF_FOLDER = os.path.join(CURRENT_DIR, 'pdfs')
    JS_FOLDER = os.path.join(CURRENT_DIR, 'js')
    JSON_FILE = os.path.join(JS_FOLDER, 'newsletters.json')
else:
    # Standardowe ścieżki względne dla Windows
    PDF_FOLDER = 'pdfs'
    JSON_FILE = 'js/newsletters.json'

def update_newsletters_json():
    try:
        print(f"Uruchamiam skrypt w folderze: {os.getcwd()}")
        print(f"Ścieżka do folderu PDF: {PDF_FOLDER}")
        print(f"Ścieżka do pliku JSON: {JSON_FILE}")
        
        # Upewnij się, że folder js istnieje
        if is_wsl:
            os.makedirs(JS_FOLDER, exist_ok=True)
        else:
            os.makedirs('js', exist_ok=True)
        print(f"Folder js istnieje lub został utworzony")
        
        newsletters = []
        
        # Sprawdź, czy folder PDF istnieje
        if not os.path.exists(PDF_FOLDER):
            print(f"Błąd: Folder {PDF_FOLDER} nie istnieje!")
            return
        
        print(f"Znaleziono folder {PDF_FOLDER}")
        pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith('.pdf')]
        print(f"Znaleziono {len(pdf_files)} plików PDF: {pdf_files}")
        
        # Znajdź wszystkie pliki PDF w folderze
        for filename in pdf_files:
            # Pełna ścieżka do pliku (do sprawdzenia daty modyfikacji)
            filepath = os.path.join(PDF_FOLDER, filename)
            
            # Pobierz datę modyfikacji pliku
            mod_time = os.path.getmtime(filepath)
            
            # Utwórz tytuł z nazwy pliku
            title = filename.replace('.pdf', '')
            
            # Formatowanie dla "Cyberbezpieczny"
            if "Cyberbezpieczny" in title:
                match = re.search(r'Cyberbezpieczny nr (\d+) (\w+) (\d+)', title)
                if match:
                    num, month, year = match.groups()
                    title = f"Cyberbezpieczny nr {num} - {month} {year}"
            
            newsletters.append({
                "title": title,
                "file": filename,
                "date_modified": mod_time
            })
        
        print(f"Przygotowano dane dla {len(newsletters)} newsletterów")
        
        # Sortuj od najnowszych na podstawie daty modyfikacji
        newsletters.sort(key=lambda x: x["date_modified"], reverse=True)
        
        # Usuń pole date_modified, które było używane tylko do sortowania
        for newsletter in newsletters:
            del newsletter["date_modified"]
        
        # Zapisz do pliku JSON
        print(f"Próbuję zapisać plik JSON: {JSON_FILE}")
        
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(newsletters, f, ensure_ascii=False, indent=2)
        
        print(f"Zaktualizowano {JSON_FILE} z {len(newsletters)} newsletterami")
        
        # Sprawdź, czy plik został utworzony
        if os.path.exists(JSON_FILE):
            print(f"Plik JSON został pomyślnie utworzony: {os.path.getsize(JSON_FILE)} bajtów")
        else:
            print(f"UWAGA: Plik JSON nie istnieje po próbie zapisania!")
            
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    update_newsletters_json()
    input("Naciśnij Enter, aby zakończyć...")