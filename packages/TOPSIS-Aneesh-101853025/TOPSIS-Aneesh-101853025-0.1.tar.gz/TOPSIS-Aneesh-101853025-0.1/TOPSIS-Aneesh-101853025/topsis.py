import pandas as pd
import numpy as np
import sys
import math as m
class topsis:
    if len(sys.argv) < 5 or len(sys.argv) > 5:
        print('WRONG NUMBER OF ARGUMENTS')
        sys.exit()

    filename=sys.argv[1]
    list1 = filename.split('.')
    ext = list1[1]
    if ext != "csv":
        print("INVALID FILE EXTENSION")
        sys.exit() 

    try:
        weights = sys.argv[2]
        impacts = sys.argv[3]
        result = sys.argv[4]

        weights = list(map(float ,weights.split(',')))
        impacts = list(map(str ,impacts.split(',')))

        for i in range(len(impacts)):
            if(impacts[i] != "+" and impacts[i] != "-"):
                print("IMPACTS CAN ONLY BE '+' OR '-' ")
                sys.exit()

        dataset = pd.read_csv(filename)

        Output = dataset.copy(deep = True)

        data=dataset.iloc[ :,1:].values.astype(float)

        (r,c)=data.shape

        if c<2:
            print("INPUT FILE DOES NOT CONTAIN ENOUGH COLUMNS")
            sys.exit()

        if len(weights) != c or len(impacts) != c:
            print("WRONG NUMBER OF WEIGHTS OR IMPACTS")
            sys.exit()

        s=sum(weights)

        for i in range(c):
            weights[i]/=s

        a=[0]*(c)

        for j in range(0,c):
          for i in range(0,r):
            a[j]=a[j]+(data[i][j]*data[i][j])

        for j in range(c):
            a[j]=m.sqrt(a[j])

        for i in range(r):
            for j in range(c):
                data[i][j]/=a[j]
                data[i][j]*=weights[j]

        ideal_positive=np.amax(data,axis=0) 
        ideal_negative=np.amin(data,axis=0)

        for i in range(len(impacts)):
            if(impacts[i]=='-'):            
                temp=ideal_positive[i]
                ideal_positive[i]=ideal_negative[i]
                ideal_negative[i]=temp

        dist_pos=list()
        dist_neg=list()

        for i in range(r):
            s=0
            for j in range(c):
                s+=pow((data[i][j]-ideal_positive[j]), 2)

            dist_pos.append(float(pow(s,0.5)))

        for i in range(r):
            s=0
            for j in range(c):
                s+=pow((data[i][j]-ideal_negative[j]), 2)

            dist_neg.append(float(pow(s,0.5)))

        performance_score=dict()

        for i in range(r):
            performance_score[i+1]=dist_neg[i]/(dist_neg[i]+dist_pos[i])

        a=list(performance_score.values())
        b=sorted(list(performance_score.values()) , reverse=True)

        rank=dict()

        for i in range(len(a)):
            rank[(b.index(a[i]) + 1)] = a[i]
            b[b.index(a[i])] = -b[b.index(a[i])]

        row=list(i+1 for i in range(len(b)))
        a=list(rank.values())
        rr=list(rank.keys())

        Output['TOPSIS Score'] = a
        Output['Rank'] = rr

        Output.to_csv(result, index = False)

        # print(Output.to_string(index=False))

    except ValueError:
        print("WEIGHTS CAN ONLY BE NUMERIC")

    except FileNotFoundError:
        print("NO SUCH FILE EXISTS!!")

if __name__ == "__main__":
    topsisClass()