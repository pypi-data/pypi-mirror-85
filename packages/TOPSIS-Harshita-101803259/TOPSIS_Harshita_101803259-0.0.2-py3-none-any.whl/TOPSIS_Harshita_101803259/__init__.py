def main():
    import pandas as pd
    import math as m
    import copy
    import sys
    import os
    if(len(sys.argv)!=5):
        raise  Exception("you did not enter the correct parameters ")
    ext = os.path.splitext(sys.argv[1])[-1].lower()
    ext1 = os.path.splitext(sys.argv[4])[-1].lower()
    if(ext!='.csv' or ext1!='.csv'):
        raise Exception("you entered wrong filepath")
    try:
        file=open(sys.argv[1])
    except FileNotFoundError:
        raise Exception("File u entered doesn't exist")
    file=pd.read_csv(sys.argv[1])
    weights=sys.argv[2]
    impact=sys.argv[3]
    test=weights.split(",")
    test1=[i for i in weights if(i in ',')]
    weights=test
    if(len(file.columns)<3):
        raise Exception("your file does not contain  three or more than three columns")
    if(len(file.columns)-1 != len(file._get_numeric_data().axes[1])):
        raise Exception("except first column every column must have a numeric data")
    if(len(test)-1!=len(test1)):
        raise Exception("there is some error in weights.they must be seperated by ','")
    test=[i for i in impact if(i not in ',')]
    test1=[i for i in impact if(i in ',')]
    if(len(test)-1!=len(test1)):
        raise Exception("there is some error in impact.they must be seperated by ','")
    impact=impact.replace(',','')
    if(len(file.columns)-1 != len(weights)):
        raise Exception("the weights entered are not equal to the columns")
    if(len(file.columns)-1 != len(impact)):
        raise Exception("the impact entered are not equal to the columns")
    test=[i for i in impact if(i not in '+-')]
    if(len(test)>0):
        raise Exception("data entered in impact should be + or -")
    test=[file.columns[i] for i in range(1,len(file.columns)) ]
    store=[]
    mm=0
    cal=[]
    st=[]
    vplus=[]
    vminus=[]
    for i in test:
        sum=0
        for j in file[i]:
            sum=sum+pow(j,2)
        store.append(m.sqrt(sum))
        cal=[]        
        for k in file[i]:
            k=k/store[mm]
            cal.append(k*float(weights[mm]))
        if(impact[mm]=='+'):
            vplus.append(max(cal))
            vminus.append(min(cal))
        if(impact[mm]=='-'):
            vplus.append(min(cal))
            vminus.append(max(cal))
        st.append(cal)
        mm+=1
    splus=[]
    sminus=[]
    perf=[]
    for mm in range(0,len(st[0])):
        sum=0
        di=0
        strr=-1
        for i in st:
            strr+=1
            sum=sum+pow(i[mm]-vplus[strr],2)
            di=di+pow(i[mm]-vminus[strr],2)
        splus.append(m.sqrt(sum))
        sminus.append(m.sqrt(di))
        perf.append(sminus[mm]/(splus[mm]+sminus[mm]))
    t=copy.deepcopy(perf)
    t.sort(reverse=True)
    rank=[]
    for i in  perf:
        ll=t.index(i)
        rank.append(ll+1)
    result = pd.DataFrame()
    result=file.copy(deep=True)
    result['Topsis Score']=perf
    result['Rank']=rank
    result.to_csv(sys.argv[4],index=False)