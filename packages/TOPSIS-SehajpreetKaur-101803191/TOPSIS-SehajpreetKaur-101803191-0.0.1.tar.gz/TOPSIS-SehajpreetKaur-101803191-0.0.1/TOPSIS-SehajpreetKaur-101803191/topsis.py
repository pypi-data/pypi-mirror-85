import pandas as pd
import os
import sys

def main():
    if len(sys.argv) != 5:
        print("Wrong number of parameters")
        print("Usage: python topsis.py <InputDataFile> <Weights> <Impacts> <ResultFileName>")
        exit(1)

    a=[sys.argv[1],sys.argv[4]]
    for i in a: 
        temp=i.split('.')
        if temp[1]!="csv":
            print("input file should be of csv type")
            sys.exit(1)
    d1, d2 = pd.read_csv(sys.argv[1]), pd.read_csv(sys.argv[1])

    if os.path.exists(sys.argv[1]) == False:   
        print("File not Found")
        sys.exit(1)
    else:
        d1, d2 = pd.read_csv(sys.argv[1]), pd.read_csv(sys.argv[1])
        col = len(d2.columns.values)

        if col < 3:
            raise Exception("Invalid number of columns( less than 3 )")
        
        try:
            weights = sys.argv[2].split(",")
            impact = sys.argv[3].split(",")
        except:
            raise Exception("weights and impact must be seperated by commas")

        if((len(weights) != len(impact)) and (len(weights) != col)):
            print("Length of weight, columns and impact not equal")
            exit()

        for i in impact:
            if i not in ["+", "-"]:
                print("impact can only be positive or negative")
                exit()

        for i in range(1, col):
            pd.to_numeric(d1.iloc[:, i], errors='coerce')
            d1.iloc[:, i].fillna(
                (d1.iloc[:, i].mean()), inplace=True)

        try:
            weights = [int(i) for i in sys.argv[2].split(',')]
        except:
            raise Exception("Error in weights array !")

        for i in range(1, col):
            temp = 0
            for j in range(len(d2)):
                temp = temp + d2.iloc[j, i]**2
            temp = temp**0.5
            for j in range(len(d2)):
                d2.iat[j, i] = (
                    d2.iloc[j, i] / temp)*weights[i-1]

        pos = (d2.max().values)[1:]
        neg = (d2.min().values)[1:]
        for i in range(1, col):
            if impact[i-1] == '-':
                pos[i-1], neg[i-1] = neg[i-1], pos[i-1]
        score = []
        for i in range(len(d2)):
            testPos, te = 0, 0
            for j in range(1, col):
                testPos = testPos + (pos[j-1] - d2.iloc[i, j])**2
                te = te + (neg[j-1] - d2.iloc[i, j])**2
            testPos, te = testPos**0.5, te**0.5
            score.append(te/(testPos + te))
        d1["TOPSIS SCORE"] = score

        d1["RANK"] = (d1["TOPSIS SCORE"].rank(method='max', ascending=False))
        d1 = d1.astype({"RANK": int})

        d1.to_csv(sys.argv[4], index=False)

if __name__ == "__main__": 
    main()
