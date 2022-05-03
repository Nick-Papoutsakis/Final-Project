import os, requests, time, json
import pandas as pd

def get_hero_stats():
    herodata = requests.get("https://api.opendota.com/api/heroStats").json()
    pd.DataFrame(herodata).to_csv("hero_stats.csv", sep=",")
    with open("hero_stats.json", "w") as outputfile:
        json.dump(herodata, outputfile)

get_hero_stats()
