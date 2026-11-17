from csv import DictReader
from typing import List, Dict

with open("Holdmybeer_data/ratings.csv", "r", encoding="utf8") as file:
    table = list(DictReader(file))

print(table)