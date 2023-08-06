import copy
import csv
import math
import os
import pandas
import sys

def topsis():
    n=len(sys.argv)
    if(n<=4):
        print("Wrong number of Arguments passed!!")
        print("Usages:python topsis.py <Input> <Weights> <Impacts> <ResName>")
        print("Example:python topsis.py input.csv 1,1,1,2 +,+,-,+ result.csv")
        exit(0)
    if (os.path.exists(sys.argv[1])==False):
        print(sys.argv[1]+"File doesn't exists")
        exit(0)
    inputf=pandas.read_csv(sys.argv[1])
    n=inputf.shape[1]-1
    if(n<3):
        print("Atleast 3 cols required")
        exit(0)
    weights=[]
    impacts=[]
    inpW=sys.argv[2]
    inpI=sys.argv[3]
    res=sys.argv[4]
    wlength=len(inpW)
    implength=len(inpI)
    i=0
    while i!=wlength:
        if(inpW[i]!=','):
            num=0
            cnt=0
            flag=0
            while(inpW[i]!=','):
                if(inpW[i]=='.'):
                    if(flag==1):
                        print("Multiple decimals in a number are not valid")
                        exit(0)
                    flag=1
                    i+=1
                    continue
                w=int(inpW[i])
                if(w>=0 and w<=9):
                    num=num*10+w
                    i+=1
                    if(flag==1): cnt+=1
                    if(i==wlength): break
                else:
                    print("Weights should be separated by ','")
                    exit(0)
            cnt=10**cnt
            num=num/cnt
            weights.append(num)
        elif(inpW[i]==','): i+=1
        else:
            print("Weights should be separated by ','")
            exit(0)
    flag=0
    for i in range (0,implength):
        if(inpI[i]=='+'):
            if(flag==1):
                print("Consecutive +/- operators without ','")
                exit(0)
            else:
                flag=1
                impacts.append(1)
        elif(inpI[i]=='-'):
            if(flag==1):
                print("Consecutive +/- operators without ','")
                exit(0)
            else:
                impacts.append(-1)
                flag=1
        elif(inpI[i]==','):
            if(flag==0):
                print("Consecutive ','")
                exit(0)
            else:
                flag=0
                continue
        else:
            print("Impacts aren't in +/-")
            exit(0)
    if(n!=len(weights)):
        print("Number of weights and columns are not same")
        exit(0)
    if(n!=len(impacts)):
        print("Number of impacts and columns are not same")
        exit(0)
    models=inputf.shape[0]
    cols=list(inputf.columns)
    inputf=inputf.values.tolist()
    data=copy.deepcopy(inputf)
    for j in range(1,n+1):
        num=0
        for i in range (0,models):
            if(isinstance(inputf[i][j], str)):
                print("Invalid data")
                exit(0)
            else:
                num+=inputf[i][j]*inputf[i][j]
        num=math.sqrt(num)
        for i in range (0,models):
            inputf[i][j]=inputf[i][j]/num
    
    for j in range(1,n+1):
        for i in range (0,models):       
            inputf[i][j]=inputf[i][j] * weights[i-1]   
    ibest=[]
    iworst=[]
    for j in range(1,n+1):
        maxi=inputf[0][j]
        mini=inputf[0][j]
        for i in range (1,models):
            mini=min(mini,inputf[i][j])
            maxi=max(maxi,inputf[i][j])
        if(impacts[j-1]==1):
            ibest.append(maxi)
            iworst.append(mini)
        else:
            ibest.append(mini)
            iworst.append(maxi)
    sbest=[]
    sworst=[]
    for i in range(0,models):
        num1=0
        num2=0
        for j in range (1,n+1):
            num1+=(inputf[i][j]-ibest[j-1])**2
            num2+=(inputf[i][j]-iworst[j-1])**2
        num1=math.sqrt(num1)
        num2=math.sqrt(num2)
        sbest.append(num1)
        sworst.append(num2)
    perf=[]
    temp=[]
    for i in range (0,models):
        p=sworst[i]/(sbest[i]+sworst[i])
        perf.append(p)
        temp.append(p) 
    rank=[]
    temp.sort(reverse=True)
    for i in range (0,models):
        j=0
        while(temp[j]!=perf[i]):
            j+=1
        rank.append(j+1)
    result=[]
    for i in range (0,models):
        l=[]
        for j in range(0,n+1):
            l.append(data[i][j])
        l.append(perf[i])
        l.append(rank[i])
        result.append(l)
    cols.append("Topsis Score")
    cols.append("Rank")
    rcsv=open(res,'x')          
    fields=cols         
    csvwriter = csv.writer(rcsv)
    csvwriter.writerow(fields)
    csvwriter.writerows(result)
    rcsv.close()
    
if __name__ == "__main__":
    topsis() 
print("Completed!!!😁😁😁")