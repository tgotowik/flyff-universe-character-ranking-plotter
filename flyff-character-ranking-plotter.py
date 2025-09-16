import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

DEBUG = False

TODAY = datetime.today().strftime('%Y-%m-%d')

SERVERS = {
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

        # find table class
        table = soup.find("table", class_="table")

        # find tbody
        tbody = table.find("tbody") if table.find("tbody") else table

        # read table rows
        rows = tbody.find_all("tr")

        data = []

        for row in rows:
            cols = row.find_all(["td", "th"])  # get all columns
            cols = [col.text.strip() for col in cols]  # extract

            if len(cols) > 2: 
                key = cols[2]  # 3 value is key

                # if key not exists + 1
                level[key] = level.get(key, 0) + 1

            if cols[3].split()[0] in class_counts:
                class_counts[cols[3].split()[0]] = class_counts.get(cols[3].split()[0], 0) + 1

            data.append(cols)

    if DEBUG == True:
        print(server_id)
        print(level)
        print(class_counts)
    return level, class_counts

def new_plot(df):
    # create figure and axes
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # define color for each class
    colors = ['#ff6767', '#db3131', '#737aff', '#474dc2', '#49de72', '#6bc16c', '#945eff', '#5500ff']

    # create plot
    df.plot(kind='bar', stacked=True, ax=ax, color=colors)
    
    # titel and axes description
    plt.title("Verteilung der Klassen auf den Servern")
    plt.xlabel("Server")
    plt.ylabel("Anzahl")
    plt.xticks(rotation=45)

    # create legend
    plt.legend(title="Klassen", bbox_to_anchor=(1, 1), loc='upper left')

    plt.tight_layout()

    # Insert numbers into the respective bar sections.
    for p in ax.patches:
        height = p.get_height()
        if height > 0:  # Prevents zero values from being displayed
            x = p.get_x() + p.get_width() / 2
            y = p.get_y() + height / 2
            ax.text(x, y, str(int(height)), ha='center', va='center', fontsize=10, color='white')

    # Save plots to data
    plt.savefig(f'plots/{TODAY}-flyff-universe-character-ranking-plot.png', bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    mapped_data = {}

    # get class and level data each server
    for server in SERVERS:
        level_data, class_data = get_server_info(SERVERS[server])

        # error when no data was fetched
        if level_data is None or class_data is None:
            print(f"Error: Did not fetch data for: {server}")
            continue 

        # map server to classes
        for class_name, class_value in class_data.items():
            if class_name not in mapped_data:
                mapped_data[class_name] = {}
            mapped_data[class_name][server] = class_value

    # make panda frame
    df = pd.DataFrame(mapped_data)

    if DEBUG == True:
        print(df)

    new_plot(df)
