import pandas as pd
import sys
import os

def handle_errors():
    if len(sys.argv)!=5:
        raise Exception("Incorrect no. of parameters\nInput format is python topsis.py <InputDataFile> <Weights> <Impacts> <ResultFileName>")
    if not os.path.isfile(sys.argv[1]):
        raise Exception(sys.argv[1]+" file doesn't exist\nRecheck filename or directory and try again!")    
    if not sys.argv[1].endswith(".csv"):
        raise TypeError("Input file format must be csv")
        
def main():
    handle_errors()
    df=pd.read_csv(sys.argv[1])
    wgt=list(sys.argv[2].split(","))
    impact=list(sys.argv[3].split(","))
    col=len(df.columns)-1
    if col<2:
        raise Exception(sys.argv[1]," must contain 3 or more columns")
    if len(wgt)!=col:
        raise Exception("No. of weights provided doesn't match with no. of parameters.\nNote: Weights must be comma separated")
    if len(impact)!=col:
        raise Exception("No. of impacts provided doesn't match with no. of parameters.\nNote: Impacts must be comma separated")
    for i in range(len(wgt)):
        try:
            wgt[i]=float(wgt[i])
        except:
            raise TypeError("Invalid weights entered\nEnter comma separated numeric weights\nEg,'0.25,0.25,0.25,0.25'")
    for i in impact:
        if i!='+' and i!='-':
            raise TypeError("Invalid impacts entered\nEnter comma separated array of '+' and '-'\nEg,'+,+,+,-'")
    Sp_df=pd.DataFrame()
    Sm_df=pd.DataFrame()
    for i in range(col):
        c=df.iloc[:,i+1]
        if c.dtype!='int64' and c.dtype!='float64':
            raise Exception("Data provided must be numeric")
        c=list(c)
        sum=0
        for j in c:
            sum=sum+j*j
        sum=pow(sum,0.5)
        for j in range(len(c)):
            c[j]=(c[j]/sum)*wgt[i]
        l=[]
        if impact[i]=="-":
            l=[min(c),max(c)]
        else:
            l=[max(c),min(c)]
        sp=[]
        sm=[]
        for j in range(len(c)):
            sp.append(pow((c[j]-l[0]),2))
            sm.append(pow((c[j]-l[1]),2))
        Sp_df.insert(i,i+1,sp,True)
        Sm_df.insert(i,i+1,sm,True)
    Sp=Sp_df.sum(axis=1)
    Sm=Sm_df.sum(axis=1)
    c=[]
    for i in range(len(Sp)):
        score=pow(Sm[i],0.5)/(pow(Sp[i],0.5)+pow(Sm[i],0.5))
        c.append(score)
    df["Topsis Score"]=c
    df["Rank"]=df["Topsis Score"].rank()
    df["Rank"]=df["Rank"].astype(int)
    df.to_csv(sys.argv[4],index=False)
          
if __name__=="__main__":
    main()
    