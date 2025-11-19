import pandas as pd
import math
def updateConsensus(chartTitle):

    # read the number of charts for the chartTitle so we can do a weighted average against the current consensus
    db = pd.read_csv(f'src/alignments/{chartTitle}.csv')
    weight = len(db)
    numCharts = weight -1

    # the new chart is the last row of the csv
    newChart = list(db.iloc[numCharts])[2:]
    author = list(db.iloc[numCharts])[0]

    # read the current consensus
    df = pd.read_csv(f'src/alignments/{chartTitle}Consensus.csv')
    try:
        currentConsensus = list(df.iloc[0])
    except Exception as e:
        # there isn't a consensus yet
        currentConsensus = newChart

    # print(newChart, currentConsensus)
    # calculate the new consensus as a weighted average between the new chart and the current consensus
    # also begin to calculate the temperature as 1 - cosine similarity
    newConsensus = []
    dotProduct = 0
    userMagnitude = 0
    consensusMagnitude = 0
    for i in range(len(newChart)):
        # print(i, newChart[i], currentConsensus[i])
        

        # in some cases this will just replace unranked with unranked, like in the case of the first ever submitted chart having unranked elements. That's fine.
        if currentConsensus[i] == 'unranked':
            currentConsensus[i] = newChart[i]

        if newChart[i] == 'unranked':
            continue

        left = min(100,max(0,int(newChart[i].split(';')[0]))) - 50
        right = min(100,max(0,int(newChart[i].split(';')[1]))) - 50
        consensusLeft = int(currentConsensus[i].split(';')[0]) - 50
        consensusRight = int(currentConsensus[i].split(';')[1]) - 50

        newConsensus.append(f"{int((50 + left + ((consensusLeft + 50) * numCharts)) / weight)};{int((50 + right + ((consensusRight + 50) * numCharts)) / weight)}")

        dotProduct += left * consensusLeft + right * consensusRight
        userMagnitude += left * left + right * right
        consensusMagnitude += consensusLeft * consensusLeft + consensusRight * consensusRight

    temperature = int((1 - (dotProduct / max(math.sqrt(userMagnitude) * math.sqrt(consensusMagnitude), 0.000001))) * 100)

    print("Temperature: " + str(temperature))
    print(newConsensus)

    # write the new consensus to the csv
    df.loc[0] = newConsensus
    df.to_csv(f'src/alignments/{chartTitle}Consensus.csv', index=False)

    # add the temperature to the new chart
    newChart.insert(0, author)
    newChart.insert(1, str(temperature))

    print(newChart)
    db.iloc[numCharts] = newChart

    # update the other temperatures
    # if there's only one entry in the db return because we already calculated the temperature
    if len(db) == 1:
        db = db.copy()
        db.to_csv(f'src/alignments/{chartTitle}.csv', index=False)
        return
    
    print("Updating temperatures for the previous " + str(len(db) - 1) + " charts")
    for i in range(len(db) - 1):
        dotProduct = 0
        userMagnitude = 0
        consensusMagnitude = 0
        for j in range(len(currentConsensus)):

            if currentConsensus[j] == 'unranked' or db.iloc[i][int(j + 2)] == 'unranked':
                continue

            left = min(100,max(0,int(db.iloc[i][int(j + 2)].split(';')[0])))-50
            right = min(100,max(0,int(db.iloc[i][int(j + 2)].split(';')[1])))-50
            consensusLeft = int(currentConsensus[j].split(';')[0])-50
            consensusRight = int(currentConsensus[j].split(';')[1])-50
            dotProduct += left * consensusLeft + right * consensusRight
            userMagnitude += left * left + right * right
            consensusMagnitude += consensusLeft * consensusLeft + consensusRight * consensusRight

        temperature = int((1 - (dotProduct / max(math.sqrt(userMagnitude) * math.sqrt(consensusMagnitude), 0.000001))) * 100)
        print(i, temperature)
        # replace the temperature in the db
        db.at[i, "Temperature"] = str(temperature)
        db = db.copy()
        print(db.iloc[i])

    # write the new chart to the csv, replacing the old one
    
    db.to_csv(f'src/alignments/{chartTitle}.csv', index=False)

    return

# literally just calculates the consensus as the average of EVERY response on the chart.
def recalculateConsensus(chartTitle):
    db = pd.read_csv(f'src/alignments/{chartTitle}.csv')
    consensus = []
    # print(len(db.columns), len(db))
    # print(db.iloc[0][2:])
    # print(len(db.columns) - 2)
    for i in range(2, len(db.columns)):
        left = 0
        right = 0
        unranked = 0
        for j in range(len(db)):
            if db.iloc[j][i] == 'unranked':
                unranked += 1
                continue
            # print(db.iloc[j][i])
            left += int(db.iloc[j][i].split(';')[0])
            right += int(db.iloc[j][i].split(';')[1])

        if unranked == len(db):
            consensus.append('unranked')
            continue

        # print(left / len(db), right / len(db))
        consensus.append(f"{int(left / (len(db) - unranked))};{int(right / (len(db) - unranked))}")
    print(consensus)

    df = pd.read_csv(f'src/alignments/{chartTitle}Consensus.csv')
    df.loc[0] = consensus
    df.to_csv(f'src/alignments/{chartTitle}Consensus.csv', index=False)

def updateOutOfDateTemperatures(chartTitle):

    # read the db and current consensus
    db = pd.read_csv(f'src/alignments/{chartTitle}.csv')
    
    # if there's only one entry in the db return because we already know the temperature is 0
    if len(db) == 1:
        return
    
    df = pd.read_csv(f'src/alignments/{chartTitle}Consensus.csv')
    
    currentConsensus = list(df.iloc[0])

    # calculate the temperature for each chart in the db
    for i in range(len(db)):
        dotProduct = 0
        userMagnitude = 0
        consensusMagnitude = 0
        for j in range(len(currentConsensus)):

            if currentConsensus[j] == 'unranked' or db.iloc[i][j + 2] == 'unranked':
                continue

            left = min(100,max(0,int(db.iloc[i][j + 2].split(';')[0]))) - 50
            right = min(100,max(0,int(db.iloc[i][j + 2].split(';')[1]))) - 50
            consensusLeft = int(currentConsensus[j].split(';')[0]) - 50
            consensusRight = int(currentConsensus[j].split(';')[1]) - 50
            dotProduct += (left * consensusLeft) + (right * consensusRight)
            userMagnitude += (left * left) + (right * right)
            consensusMagnitude += (consensusLeft * consensusLeft) + (consensusRight * consensusRight)

        print(i, dotProduct, userMagnitude, consensusMagnitude)
        temperature = int((1 -  (dotProduct / max(math.sqrt(userMagnitude) * math.sqrt(consensusMagnitude), 0.000001))) * 100)
        print(i, temperature)
        db.at[i, "Temperature"] = str(temperature)

    # write the new chart to the csv, replacing the old one
    db.to_csv(f'src/alignments/{chartTitle}.csv', index=False)

    return