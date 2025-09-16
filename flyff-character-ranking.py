import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

def get_server_info(server_id):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    level = {}
    class_counts = {
        "Psykeeper": 0,
        "Elementor": 0,
        "Blade": 0,
        "Knight": 0,
        "Jester": 0,
        "Ranger": 0,
        "Ringmaster": 0,
        "Billposter": 0
    }
    for i in range(1,21):
        url = f"https://universe.flyff.com/sniegu/ranking/characters?server={server_id}&page={i}"
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "html.parser")

        # Tabelle mit der Klasse "table" finden
        table = soup.find("table", class_="table")

        # tbody finden (falls vorhanden, sonst ganze Tabelle nehmen)
        tbody = table.find("tbody") if table.find("tbody") else table

        # Tabellenzeilen (tr) auslesen
        rows = tbody.find_all("tr")

        data = []

        for row in rows:
            cols = row.find_all(["td", "th"])  # Alle Spalten holen
            cols = [col.text.strip() for col in cols]  # Text extrahieren

            if len(cols) > 2:  # Sicherstellen, dass es mind. 3 Spalten gibt
                key = cols[2]  # Den Wert aus der 3. Spalte als Key nehmen

                # Falls der Key noch nicht existiert, auf 1 setzen, sonst erhöhen
                level[key] = level.get(key, 0) + 1

            if cols[3].split()[0] in class_counts:
                class_counts[cols[3].split()[0]] = class_counts.get(cols[3].split()[0], 0) + 1

            data.append(cols)

    #print(server_id)
    #print(level)
    #print(class_counts)
    return level, class_counts

def new_plot(df):
    # Erstelle die Figur und Achse
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Definiere die Farben für die jeweiligen Klassen
    colors = ['#ff6767', '#db3131', '#737aff', '#474dc2', '#49de72', '#6bc16c', '#945eff', '#5500ff']

    # Erstelle das gestapelte Balkendiagramm mit spezifischen Farben
    df.plot(kind='bar', stacked=True, ax=ax, color=colors)
    
    # Titel und Achsenbeschriftungen
    plt.title("Verteilung der Klassen auf den Servern")
    plt.xlabel("Server")
    plt.ylabel("Anzahl")
    plt.xticks(rotation=45)

    # Legende außerhalb des Plots platzieren
    plt.legend(title="Klassen", bbox_to_anchor=(1, 1), loc='upper left')

    plt.tight_layout()

    # Füge Zahlen in die jeweiligen Balkenabschnitte ein
    for p in ax.patches:
        height = p.get_height()
        if height > 0:  # Verhindert das Anzeigen von Nullwerten
            x = p.get_x() + p.get_width() / 2
            y = p.get_y() + height / 2
            ax.text(x, y, str(int(height)), ha='center', va='center', fontsize=10, color='white')

    # Speichern des Plots in einer Datei
    plt.savefig('server_klassen_verteilung.png', bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    
    server_colors = {
        "Psykeeper": "#ff2d00",
        "Elementor": "#ff6800",
        "Blade": "#0cff00",
        "Knight": "#d62728",
        "Jester": "#9467bd",
        "Ranger": "#8c564b",
        "Rigmaster": "#e377c2",
        "Billposter": "#7f7f7f",
        "japanese": "#bcbd22",
        "chinese": "#17becf"
    }

    servers = {
        "Lawolf": "1",
        "Mia": "2",
        "Glaphan": "3",
        "Rhisis": "4",
        "Mushpoie": "5",
        "Totemia": "9",
        "Burudeng": "11",
        "Flarine": "20",
        "Japanese": "23",
        "Chinese": "25"
    }
    server_data = {}

    # Daten für Klassen und Level
    for server in servers:
        level_data, class_data = get_server_info(servers[server])

        # Überprüfe, ob die Rückgabewerte None sind
        if level_data is None or class_data is None:
            print(f"Fehler: Keine Daten für den Server {server}")
            continue 

        for class_name, class_value in class_data.items():
            if class_name not in server_data:
                server_data[class_name] = {}
            server_data[class_name][server] = class_value

    # Umwandlung in ein pandas DataFrame
    df = pd.DataFrame(server_data)

    # Anzeigen des DataFrames
    #print(df)

    new_plot(df)
