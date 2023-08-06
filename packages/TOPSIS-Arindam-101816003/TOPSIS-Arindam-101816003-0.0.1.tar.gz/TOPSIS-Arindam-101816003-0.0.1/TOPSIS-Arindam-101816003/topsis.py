import numpy as np
import pandas as pd
import sys
import math as m

def main():
    if len(sys.argv)!=5:
        print('Error! Wrong number of arguments passsed')
        sys.exit()
    try:
        dataset = pd.read_csv(sys.argv[1])
    except:
        print('Error! File not found')
        sys.exit

    data = dataset.iloc[:,1:].values              
    weights = sys.argv[2].split(',')        
    weights = [float(i) for i in weights]      
    impacts = sys.argv[3].split(',')        

    r, c = data.shape
    if c <= 2:
        print('Error! Input file must have atleast 3 columns')
    if len(weights) != c:
        print('Error! Number of weights are wrongly passed')
        sys.exit()
    if len(impacts) != c:
        print('Error! Number of impacts are wrongly passed')
        sys.exit()
    for i in weights:
        if i <= 0:
            print('Error! Weights must be positive')
            sys.exit()
    for i in impacts:
        if i not in ['+', '-']:
            print('Impacts must be either "+" or "-"')
            sys.exit()

    sum_weights = np.sum(weights)
    for i in range(c):
        weights[i]/=sum_weights
    
    denom = [0]*c
    
    for i in range(r):
        for j in range(c):
            denom[j] += (data[i][j]**2)
    
    for i in range(c):
        denom[i] = denom[i]**(1/2)
    
    for i in range(r):
        for j in range(c):
            data[i][j] = (data[i][j]/denom[j])*weights[j]

    ideal_best = np.amax(data,axis = 0)
    ideal_worst = np.amin(data,axis = 0)
    for i in range(c):
        if impacts[i] == '-':
            ideal_best[i], ideal_worst[i] = ideal_worst[i], ideal_best[i]
    
    dist_best = []
    dist_worst = []

    for i in range(r):
        sq_dist = 0
        for j in range(c):
            sq_dist += (data[i][j] - ideal_best[j])**2
        dist_best.append(sq_dist**(1/2))            
    
    for i in range(r):
        sq_dist = 0
        for j in range(c):
            sq_dist += (data[i][j] - ideal_worst[j])**2
        dist_worst.append(sq_dist**(1/2))
    
    performance_score = [0]*r

    for i in range(r):
        performance_score[i] = dist_worst[i]/(dist_worst[i] + dist_best[i])
    
    score_sorted = sorted(performance_score, reverse = True)

    rank = dict()

    for x in performance_score:
        rank[(score_sorted.index(x)) + 1] = x
        score_sorted[score_sorted.index(x)] = -score_sorted[score_sorted.index(x)]

    output = dataset
    output['Topsis Score'] = list(rank.values())
    output['Rank'] = list(rank.keys())

    output_file = pd.DataFrame(output)
    output_file.to_csv(sys.argv[4])

if __name__ == '__main__':
    main()