import os
from flask import Flask, render_template
import pandas as pd
import json

app = Flask(__name__, template_folder='src', static_folder='src')

@app.route("/")
def index():
    # open the alignment chart masterlist .txt and read it line by line
    with open('src/alignments/alignmentMasterlist.txt') as f:
        charts = f.readlines()
    
    for i in range(len(charts)):
        charts[i] = charts[i].split(';')
    
    # print(charts)

    return render_template('index.html', charts=charts)

@app.route("/charts<chartTitle>")
def charts(chartTitle):
    with open(f'src/alignments/{chartTitle}.json') as f:
        data = json.load(f)

    df=pd.read_csv(f'src/alignments/{chartTitle}.csv')
    creators = df['Creator'].to_list()

    return render_template('charts.html', title=data['chartTitle'], creators=creators, chart=chartTitle)



@app.route("/view<chartTitle>/<creator>")
def view(chartTitle, creator):
    print("Fetching chart for " + chartTitle + " by " + creator)
    df = pd.read_csv(f'src/alignments/{chartTitle}.csv')

    # find the row that matches the creator name
    try:
        row = list(df.loc[df['Creator'] == creator].iloc[0])
    except Exception as e:
        print(e)
        return render_template('404.html')
    try:
        with open(f'src/alignments/{chartTitle}.json') as f:
            data = json.load(f)
    except Exception as e:
        print(e)
        return render_template('404.html')

    elements = []
    titles = df.columns[1:]
    # print(titles)

    for i in range(0,len(titles)):
        if (str(row[i+1]) != "nan"):
            elements.append({
                'title': titles[i],
                'url': data[titles[i]],
                'coords': row[i+1]
            })
        else:
            break
    
    # print(row)
    # print(elements)
    return render_template('view.html', q1=data['q1'], q2=data['q2'], q3=data['q3'], q4=data['q4'], chartTitle=data['chartTitle'], chartSubtitle=creator, elements=elements)

def main():
    app.run(port=int(os.environ.get('PORT', 80)))

if __name__ == "__main__":
    main()
