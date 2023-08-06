import pandas as pd
import  numpy as np
import sys
import math as m

def main():

    if len(sys.argv) < 5:
        print('Wrong number of parameters passed');
        print("TIP FOR THE INPUT: python topsis.py <InputDataFile> <Weights> <Impacts> <ResultFileName>")
        sys.exit()

    file=sys.argv[1]
    Weights = sys.argv[2]
    Impacts = sys.argv[3]
    Result = sys.argv[4]

    try:
        Weights = list(map(float ,Weights.split(',')))
        Impacts = list(map(str ,Impacts.split(','))) 
    except:
        print('Weights or Impacts are not provided in proper format ')
        sys.exit()
        
    for each in Impacts :
        if each not in ('+','-'):
            print('Impacts are not provided in proper format ')
            sys.exit()

    try:
        InputDataFile = pd.read_csv(file)
    
    except:
        print(file+' File not found');
        sys.exit()
        
    if len(list(InputDataFile.columns))<=2:
        print('Input file should contain 3 or more columns '+ file)
        sys.exit()
    
    data=InputDataFile.iloc[ :,1:]
    
    (rows,cols)=data.shape
    data=data.values.astype(float)
    sum_of_Weights=np.sum(Weights)

    
    if len(Weights) != cols:
        print("Number of Weights are sparse")
        sys.exit()
        
    if len(Impacts) != cols:
        print("Number of Impacts are sparse")
        sys.exit()

    for i in range(cols):
        Weights[i]/=sum_of_Weights


    a=[0]*(cols)

    for i in range(0,rows):
        for j in range(0,cols):
            a[j]+=(data[i][j]*data[i][j])

    for j in range(cols):
        a[j]=m.sqrt(a[j])
        
        
    #weighted normalised decision matrix
    for i in range(rows):
        for j in range(cols):
            data[i][j]/=a[j]
            data[i][j]*=Weights[j]


    

    ideal_best=np.amax(data,axis=0) 
    ideal_worst=np.amin(data,axis=0) 
    for i in range(len(Impacts)):
        if(Impacts[i]=='-'):         
            temp=ideal_best[i]
            ideal_best[i]=ideal_worst[i]
            ideal_worst[i]=temp

    dist_pos=list()
    dist_neg=list()

    for i in range(rows):
        sq_sum=0
        for j in range(cols):
            sq_sum+=pow((data[i][j]-ideal_best[j]), 2)

        dist_pos.append(float(pow(sq_sum,0.5)))


    for i in range(rows):
        sq_sum=0
        for j in range(cols):
            sq_sum+=pow((data[i][j]-ideal_worst[j]), 2)

        dist_neg.append(float(pow(sq_sum,0.5)))


    performance_score=dict()

    for i in range(rows):
        performance_score[i+1]=dist_neg[i]/(dist_neg[i]+dist_pos[i])

    actual=list(performance_score.values())
    sort=sorted(list(performance_score.values()) , reverse=True)

    rank=dict()

    for val in actual:
        rank[(sort.index(val) + 1)] = val
        sort[sort.index(val)] =-sort[sort.index(val)]


    output=InputDataFile
    output['Topsis_score']=list(rank.values())
    output['Rank']=list(rank.keys())


    
    
    res=pd.DataFrame(output)
    res.to_csv(Result,index=False)

main()