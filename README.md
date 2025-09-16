# flyff-universe-character-ranking-plotter

This character ranking plotter is made for https://www.twitch.tv/spielestyler and his monthly character rankings.
Of course, anyone else can use it too.

# Use
- Install python, depends on your os.
- Create plot on real time data via ```python3 flyff-character-ranking-plotter.py --new-plot```
    - This will create a generated plot to the plots directory
- Spielestyler mode to read in his "Daten" Sheet
    - Since Spielestyler uses MS Excel to save his data, there is a Spielestyler importer
    - To use that save your "Daten.xlsx" as "Daten.csv" (CSV UTF-8)
    - Put that csv file in the root directory
    - Call ```python3 flyff-character-ranking-plotter.py --import-csv ./Daten.csv```
    - This will generate plots from all collected data to plots/spielestyler

# To Do:
- [ ] Fonts for Japanese and Chinese server to keep original names
- [ ] Long term plots