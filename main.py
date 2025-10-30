import os
from flask import Flask, render_template, request
import pandas as pd
import json
import html

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

    # get the data for the table
    with open(f'src/alignments/{chartTitle}.json') as f:
        data = json.load(f)

    df=pd.read_csv(f'src/alignments/{chartTitle}.csv')
    authors = df['Creator'].to_list()
    temperatures = df['Temperature'].to_list()

    charts = []
    for i in range(len(authors)):
        charts.append({
            'author': authors[i],
            'temperature': temperatures[i]
        })

    df = pd.read_csv(f'src/alignments/{chartTitle}Consensus.csv')

    elements = []
    titles = df.columns[1:]
    row = list(df.iloc[0])

    for i in range(0,len(titles)):
        if (not str(row[i+1]) in ['nan', 'unranked']):
            elements.append({
                'title': titles[i],
                'url': data[titles[i]],
                'coords': row[i+1]
            })
        else:
            break

    return render_template('charts.html', title=data['displayTitle'], charts=charts, chartTitle=chartTitle, q1=data['q1'], q2=data['q2'], q3=data['q3'], q4=data['q4'], lowx=data['lowx'], highx=data['highx'], lowy=data['lowy'], highy=data['highy'], consensus=elements)



@app.route("/view<chartTitle>/<creator>")
def view(chartTitle, creator):
    print("Fetching chart for " + chartTitle + " by " + creator)

    # find the row that matches the creator name
    try:
        df = pd.read_csv(f'src/alignments/{chartTitle}.csv')
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
    titles = df.columns[2:]
    # print(titles)

    for i in range(0,len(titles)):
        if (not str(row[i+1]) in ['nan', 'unranked']):
            elements.append({
                'title': titles[i],
                'url': data[titles[i]],
                'coords': row[i+1]
            })
        else:
            break
    
    # print(row)
    # print(elements)
    return render_template('view.html', q1=data['q1'], q2=data['q2'], q3=data['q3'], q4=data['q4'], lowx=data['lowx'], highx=data['highx'], lowy=data['lowy'], highy=data['highy'], chartTitle=chartTitle, displayTitle=data['displayTitle'], chartSubtitle=creator, elements=elements)

@app.route("/make<chartTitle>", methods=['GET', 'POST'])
def make(chartTitle):
    if request.method == 'GET':
        try:
            with open(f'src/alignments/{chartTitle}.json') as f:
                data = json.load(f)
        except Exception as e:
            print(e)
            return render_template('404.html')
        
        titles = list(data.keys())[9:]
        elements = []
        for i in range(0,len(titles)):
            elements.append({
                'title': titles[i],
                'url': data[titles[i]]
            })

        return render_template('make.html', chartTitle=chartTitle, displayTitle=data['displayTitle'], q1=data['q1'], q2=data['q2'], q3=data['q3'], q4=data['q4'], lowx=data['lowx'], highx=data['highx'], lowy=data['lowy'], highy=data['highy'], elements=elements)

    if request.method == 'POST':
        
        print("Received form data")
        form = request.get_json()
        # form = request.form
        # print(form)
        # print(form.get('author'), form.get('data'))
        # get the form data and put it in the appropriate csv. 
        # form data is a json object with 1) the author name, 2) a single string of comma seperated values already formatted in the correct order for the csv

        # get the dataset and form data. We don't need pandas for this since we're just writing the whole string to line 2 of the file
        

        author = form.get('author')
        # sanitize the author name
        author = html.escape(author)

        data = form.get('data')
        # sanitize the data
        for index in range(len(data)):
            data[index] = html.escape(data[index])

        line = author + "," + ",".join(data)

        print(line)

        with open(f'src/alignments/{chartTitle}.csv', 'a') as f:
            f.write("\n" + line)

        print("Done!")
        
        return charts(chartTitle)
    

def main():
    app.run(port=int(os.environ.get('PORT', 80)))

if __name__ == "__main__":
    main()
