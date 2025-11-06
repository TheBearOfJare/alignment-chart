import pandas as pd
import json

try:
    with open(f'src/alignments/allDisney.json') as f:
        data = json.load(f)
except Exception as e:
    print(e)

titles = list(data.keys())[9:]

# read the csv and compare the json to the csv to find the missing elements
df = pd.read_csv(f'src/alignments/allDisney.csv')
definitive = df.columns[2:]
for title in definitive:
    # print(title)
    if title not in titles:
        print(title)