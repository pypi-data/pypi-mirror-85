
import pandas as pd
import sys
import math
import copy

class Topsis:
    def __init__(self, data):
        self.data = data
    def topsis(self, weights, impact):
        data2 = copy.deepcopy(self.data)
        rms = 0
        w=0
        n = len(data2.index)
        ideal_best = []
        ideal_worst = []
        
        for i in list(data2):
            maxi = 0
            mini = 1
            tot = 0
            for j in range(n):
                tot += data2[i][j]*data2[i][j]
            rms = math.sqrt(tot)
            for k in range(n):
                data2[i][k] = (data2[i][k]/rms)*weights[w]
                if data2[i][k] > maxi:
                    maxi = data2[i][k]
                if data2[i][k] < mini:
                    mini = data2[i][k]
            if impact[w] == "+":
                ideal_best.append(maxi)
                ideal_worst.append(mini)
            else:
                ideal_best.append(mini)
                ideal_worst.append(maxi)
            w+=1
            
        k = 0
        per = []
        for i in range(n):
            sip = math.sqrt(sum((data2.iloc[i,:] - ideal_best)*(data2.iloc[i,:] - ideal_best)))
            sin = math.sqrt(sum((data2.iloc[i,:] - ideal_worst)*(data2.iloc[i,:] - ideal_worst)))
            p = sin/(sip+sin)
            per.append([k, p])
            k+=1
            
        per.sort(key = lambda x : x[1], reverse = True)
        rank = 1
        for i in range(len(per)):
            per[i].append(rank)
            rank += 1
            
        per.sort(key= lambda x: x[0])
        
        per_score = []
        per_rank = []
        
        for i in range(len(per)):
            del per[i][0]
            per_score.append(per[i][0])
            per_rank.append(per[i][1])
            
        data2["Topsis Score"] = per_score
        data2["Rank"] = per_rank
        return data2


def main():
    
    if len(sys.argv) != 5:
        print(' YOU HAVE NOT GIVEN ENOUGH ARGUMENTS')
        print('''Usage:
              python topsis.py <InputDataFile> <Weights> <Impacts> <ResultFileName>''')
        sys.exit()

    filename=sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    weights = list(map(float ,weights.split(',')))
    impacts = list(map(str ,impacts.split(',')))


    dataset = pd.read_csv(filename)

    try:
        data=dataset.iloc[:,1:].values.astype(float)
    except:
        print('coulmns from 2nd to last may contain non numerical values')
        print('From 2nd to last columns must contain numeric values only (Handling of non-numeric values)')
        sys.exit()

    name = df.iloc[:,:1]
    (r,c)=data.shape

    if c < 2:
        print('Input file must contain three or more columns')
        sys.exit()

    if (len(weights) == c ) and (len(impacts) == c):
        pass
    else:
        print('Number of weights, number of impacts and number of columns (from 2nd to last columns) must be same')
        print('Also ; Impacts and weights must be separated by ‘,’ (comma).')
        sys.exit()

    for i in impacts:
        if i not in ["+", "-"]:
            print("impact can only be '+' or '-")
            sys.exit()

    s=sum(weights)
    for i in range(c):
        weights[i]/=s


    topsis = Topsis(data)
    res = topsis.topsis(weights, impacts)
    res.insert(0, "Model", name)
    out = sys.argv[4]
    res.to_csv(f"./{out}.csv", index = False)
    
    
if __name__ == '__main__':
     main()





