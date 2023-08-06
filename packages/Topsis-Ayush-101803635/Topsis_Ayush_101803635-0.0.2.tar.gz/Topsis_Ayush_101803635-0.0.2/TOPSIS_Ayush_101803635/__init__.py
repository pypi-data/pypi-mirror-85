import pandas as pd
import math as m
import sys
import os
def Topsis(l):
    

    
##    l=['py','data.csv','1,2,1,1',"+,+,-,+",'final.csv']
##    l=l[1:]
    if len(l)!=4:
        print('Wrong entries: <inputDataFile> <Weights> <Impacts> <ResultFileName>!! try again')
        exit()

    #check for file in same folder as Program
    directory = os.getcwd()
    files=list(os.listdir(directory))
    if l[0] not in files:
        print('file not found in current location : '+str(directory))
        exit()


    ##data={1:[250,200,300,275,225],2:[16,16,32,32,16],3:[12,8,16,8,16],4:[5,3,4,4,2]}
    ##print(data)
    ##df=pd.DataFrame(data)

        
    df=pd.read_csv(l[0],index_col=0)
    leng=len(df.columns)
    df.reset_index()
    #print(df)
    df2=df.copy()


    w=l[1].split(",")
    weight=[float(i) for i in w]
    #print(weight)
    impacts=l[2].split(",")
    #print(impacts)

    vplus=[]
    vminus=[]
    for x in range(leng):
        sqsos=m.sqrt(sum(map(lambda i : i * i, df.iloc[:,x]))) #sum of squares

        normval=list(map(lambda i : i/sqsos, df.iloc[:,x])) #normalised values
        
        wnval=list(map(lambda i : i*weight[x-1], normval)) #weighted  normalised values
        df2.iloc[:,x]=wnval
        
        if impacts[x]=="-": #if min is best
            vplus.append(min(df2.iloc[:,x]))   #ideal best
            vminus.append(max(df2.iloc[:,x])) #ideal worst
        else: #if max is best
            vplus.append(max(df2.iloc[:,x]))   #ideal best
            vminus.append(min(df2.iloc[:,x]))  #ideal worst

    #print(df2) #normalised weighted matrix
    #print(vplus)   
    #print(vminus)

    sp1=[]
    sm=[]
    sc=[]

    def sp (l,vp):  # to find euclidean distance  
        return(l-vp)**2

    # now findng S+ and S- values
    for x in df2.values:
        splus=m.sqrt(sum(map(sp,x,vplus)))
        
        sminus=m.sqrt(sum(map(sp,x,vminus)))
        
        score=sminus/(splus+sminus)

        #print(splus,sminus,score)

        sp1.append(splus) #adding values to table
        sm.append(sminus)
        sc.append(score)
    df2['s+']=sp1
    df2['s-']=sm
    df2['score']=sc
    df2=df2.sort_values('score',ascending=False) #order values of table by performance score

    return df2


