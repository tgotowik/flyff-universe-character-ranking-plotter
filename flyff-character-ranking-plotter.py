import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import json
import re
import argparse

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
    "リシス": "23",
    "獨眼蝙蝠": "25"
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

def new_plot(df, date=TODAY, path_spielestyler=False):
    # create figure and axes
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # define color for each class
    colors = ['#ff6767', '#db3131', '#737aff', '#474dc2', '#49de72', '#6bc16c', '#945eff', '#5500ff']

    # plt.rcParams["font.family"] = "Arial Unicode MS" # TODO: Japanese and Chinese fonts
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
    if path_spielestyler == True:
        plt.savefig(f'plots/spielestyler-plots/{date}-flyff-universe-character-ranking-plot.png', bbox_inches='tight')
    else:
        plt.savefig(f'plots/{date}-flyff-universe-character-ranking-plot.png', bbox_inches='tight')
    
    if DEBUG == True:
        plt.show()

def parse_spielestyler_file(path_csv):
    json_data = dict()

    classes_rows_number = {
        0: "Ringmaster",
        1: "Psykeeper",
        2: "Jester",
        3: "Billposter",
        4: "Elementor",
        5: "Blade",
        6: "Ranger",
        7: "Knight"
    }
    
    date_pattern = re.compile(r'^\d{2}\.\d{2}\.\d{4}')

    with open(path_csv, "r", encoding="utf-8-sig") as f:  # <- hier encoding setzen
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # If "Stand" or date_pattern was found get date
            if line.startswith("Stand ") or date_pattern.match(line):
                if line.startswith("Stand "):
                    date = line.split()[1].split(";")[0]
                elif date_pattern.match(line):
                    date = line.split(";")[0]
                if date not in json_data:
                    json_data[date] = {}
            if line.split(";")[0] in SERVERS:
                server = line.split(";")[0]
                for i, col in enumerate(line.split(";")[1:]):
                    if i < 8:
                        if classes_rows_number[i] not in json_data[date]:
                            json_data[date][classes_rows_number[i]] = {}
                        json_data[date][classes_rows_number[i]][server] = col
    return json_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Tool to plot Flyff Universe Character Ranking."
    )
    parser.add_argument(
        "--new-plot",
        action="store_true",
        help="Create new plot with latest data."
    )
    parser.add_argument(
        "--import-csv",
        type=str,
        help="Import Spielestyler data."
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Turn on debugging."
    )

    args = parser.parse_args()
    
    if args.debug:
        DEBUG = True

    if args.new_plot:
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
    if args.import_csv:
        imported_data = parse_spielestyler_file(args.import_csv)
        
        for date in imported_data:
            df = pd.DataFrame(imported_data[date]).astype(int)
            new_plot(df, date, True)
