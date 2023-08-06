#!/usr/bin/env python
# coding: utf-8

# In[1]:


def main():
    import sys
    if len(sys.argv) < 5:
        print('Wrong number of parameters passed');
        sys.exit()
    fl = sys.argv[1]
    w = sys.argv[2]
    imp = sys.argv[3]
    try:
        w = list(map(float ,w.split(',')))
        imp = list(map(str ,imp.split(','))) 
    except:
        print('Weights or Impacts are not in proper format ')
        sys.exit()
    for each in imp :
        if each not in ('+','-'):
            print('Impacts are not in proper format ')
            sys.exit()
    import pandas
    try:
        input_data = pandas.read_csv(fl)
    except:
        print(fl+' File not found');
        sys.exit()
    if len(list(input_data.columns))<=2:
        print('Input file does not contain 3 or more columns '+ fl)
        sys.exit()
    data=input_data.iloc[ :,1:]
    (rows,cols)=data.shape
    data=data.values.astype(float)
    import  numpy
    sum_of_weights=numpy.sum(w)
    if len(w) != cols:
        print("Number of weights are less")
        sys.exit()
    if len(imp) != cols:
        print("Number of impacts are less")
        sys.exit()
    for i in range(cols):
        w[i]/=sum_of_weights
    a=[0]*(cols)
    for i in range(0,rows):
        for j in range(0,cols):
            a[j]+=(data[i][j]*data[i][j])
    import math
    for j in range(cols):
        a[j]=math.sqrt(a[j])
    #weighted normalised decision matrix
    for i in range(rows):
        for j in range(cols):
            data[i][j]/=a[j]
            data[i][j]*=w[j]
    #print(data)
    ideal_best=numpy.amax(data,axis=0) 
    ideal_worst=numpy.amin(data,axis=0) 
    for i in range(len(imp)):
        if(imp[i]=='-'):         
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
    output=input_data
    output['Topsis_score']=list(rank.values())
    output['Rank']=list(rank.keys())
    res=pandas.DataFrame(output)
    finalr = sys.argv[4]
    res.to_csv(finalr,index=False)
    #print(output)
if __name__=="__main__":
    main()

