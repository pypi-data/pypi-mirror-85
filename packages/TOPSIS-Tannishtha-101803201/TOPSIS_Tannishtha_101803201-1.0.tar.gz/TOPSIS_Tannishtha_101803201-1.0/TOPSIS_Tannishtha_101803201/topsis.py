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
                tot += data2[i][j]
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
        print('''Usage:
python topsis.py <InputDataFile> <Weights> <Impacts> <ResultFileName>''')
        exit()

    inpfile = sys.argv[1]

    df = pd.DataFrame()

    try:
        df = pd.read_csv(inpfile)
    except:
        print("Input file not found")
        exit()

    weights = sys.argv[2].split(",")
    impact = sys.argv[3].split(",")

    if len(weights) < 2 or len(impact) < 2:
        print("Weights and impact should be separated by ',' or be more than 2 ")
        exit()


    if(len(weights) != len(impact)):
        print("Length of weight and impact not equal")
        exit()

    k = 0
    for i in impact:
        if i not in ["+", "-"]:
            print("impact can only be positive or negative")
            exit()
        weights[k] = int(weights[k])
        k += 1


    new_df = df.iloc[:,1:]
    name = df.iloc[:,:1]

    if len(new_df) < 2:
        print("columns not appropriate")
        exit()

    topsis = Topsis(new_df)
    res = topsis.topsis(weights, impact)
    
    res.insert(0, "Model", name)

    out = sys.argv[4]
    res.to_csv(f"./{out}.csv", index = False)
    
    
if __name__ == '__main__':
     main()