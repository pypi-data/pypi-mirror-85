if __name__ == "__main__":
    import os
    import numpy as np
    import pandas as pd
    import sys
    import copy

    if len(sys.argv) != 5:
        raise Exception('Number of params incorrect')

    dataFile = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    resultFile = sys.argv[4]

    #note : len(weights) =  number of commas + 1
    try:
        weights = np.array([x.strip() for x in weights.split(',')],dtype = float)
        impacts = np.array([x.strip() for x in impacts.split(',')],dtype = str)
    except:
        raise Exception('Invalid data entries for wieghts/impacts')
    for element in impacts:
        if element != '+' and element != '-':
            raise Exception('Incorrect Impact')

    if os.path.exists(dataFile) == False:
        raise Exception('File not Found')

    df = pd.read_csv(dataFile)
    if len(df.columns) < 3:
        raise Exception('Number of columns incorrect')

    # corr = np.array(df['Corr'])
    # rseq = np.array(df['Rseq'])
    # rmse = np.array(df['RMSE'])
    # accuracy = np.array(df['Accuracy'])
    columns_np = []

    #handling non-numeric values
    try:
        for column in df.columns[1:]:
            col = np.array(df[column],dtype = float)
            columns_np.append(col)
    except:
        raise Exception('Entries were not numeric values')

    columns_np = np.array(columns_np)
    lenCheck = len(columns_np[0])
    for col in columns_np :
        if lenCheck != len(col):
            raise Exception('Incorrect length Match')

    if (len(impacts) != len(df.columns) - 1 ) or (len(weights) != len(df.columns) - 1):
        raise Exception('Incorrect Length Match')


    #After all exceptions are handled , we are good to go =>

    topsisScore = []
    ranking = [None]*(len(df[df.columns[0]]))

    denominator = []
    for col in columns_np:
        denominator.append(np.sum(col**2))

    # finding the weighted normalized values
    print(type(weights[0]))
    for i in range(len(columns_np)):
        columns_np[i] = columns_np[i] * (weights[i] / denominator[i])

    # finding ideal best and ideal worst
    ideal_best = []
    ideal_worst = []
    for i in range(len(columns_np)):
        if impacts[i] == '+':
            ideal_best.append(np.max(columns_np[i]))
            ideal_worst.append(np.min(columns_np[i]))
        else:
            ideal_best.append(np.min(columns_np[i]))
            ideal_worst.append(np.max(columns_np[i]))

    #finding euclidean distance between ideal best and ideal worst

    for i in range(len(df[df.columns[0]])): # for each criteria object mode
        sum_best = 0
        sum_worst = 0
        for j in range(len(columns_np)): # for columns 2nd till last
            sum_best += (columns_np[j][i] - ideal_best[j]) * (columns_np[j][i] - ideal_best[j])
            sum_worst += (columns_np[j][i] - ideal_worst[j]) * (columns_np[j][i] - ideal_worst[j])

        sum_best = (sum_best ** (0.5))
        sum_worst = (sum_worst ** (0.5))
        topsisScore.append(sum_worst / (sum_best + sum_worst) )

    pseudo_score = copy.deepcopy(topsisScore)

    rank = 1
    for count in range(len(pseudo_score)):
        idx = pseudo_score.index(max(pseudo_score))
        ranking[idx] = rank
        pseudo_score[idx] = -1
        rank = rank + 1

    df_new = copy.deepcopy(df)
    df_new['Topsis Score'] = topsisScore
    df_new['Rank'] = ranking
    df_new.to_csv(resultFile,index = False)






