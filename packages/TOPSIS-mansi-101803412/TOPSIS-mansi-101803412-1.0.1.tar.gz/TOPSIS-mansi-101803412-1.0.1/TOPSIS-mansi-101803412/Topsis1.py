

import sys
import pandas as pd
import numpy as np
import scipy.stats as ss

def Topsis():
#Printing the  arguments
    print(sys.argv)

#Finding the number of arguments
    length=len(sys.argv)
    if length<5:
        print("Please Enter correct number of arguments")
        print("Try again")
        exit(0)
    else:
            try:
                df=pd.read_csv(sys.argv[1])
                if df.shape[1]<3:
                    print("No. ofcolumns in the input file should be equal to or more than 3")
                    print("Give valid file")
                    exit(0)
                for i in range(1,df.shape[1]):
                        if df.iloc[:,i].dtype=="float64":
                            continue
                        else:
                            print("Columns should be of numeric type only")
                            exit(0)
                for i in range(len(sys.argv[2])):
                    if i%2!=0:
                        if sys.argv[2][i]!=',':
                            print("Weights must be separated by commas only")
                            exit(0)
                for i in range(len(sys.argv[3])):
                    if i%2!=0:
                        if sys.argv[3][i]!=",":
                            print("Impacts must be separated by commas only")
                            exit(0)
                    else:
                        if(sys.argv[3][i]!="+") and (sys.argv[3][i]!="-"):
                            print("Impacts should be either + or - ")
                            exit(0)
                list_weights=sys.argv[2].split(",")
                list_impacts=sys.argv[3].split(",")
                list_weights=list(map(int, list_weights)) #Converting list from string type to int
                if len(list_weights) == len(list_impacts) and (df.shape[1]-1)==len(list_impacts):
            #Calculating root of sum of squares
                    list_RootofSumofSquares=[]
                    for i in range(1,df.shape[1]):
                    x= np.sqrt((df.iloc[:,i]**2).sum())
                    list_RootofSumofSquares.append(x)
                
            #Vector Normalization
            
                    k=0
                    for i in range(1,df.shape[1]):
                        df.iloc[:,i]=df.iloc[:,i].div(list_RootofSumofSquares[k])
                        k=k+1
        
        
        #Weights * Normalized Performance Value
                    k=0
                    for i in range(1,df.shape[1]):
                        df.iloc[:,i]=df.iloc[:,i].multiply(list_weights[k])
                        k+=1
            
            #Finding ideal best and ideal worst values
                    k=0
                    ideal_best=[]
                    ideal_worst=[]
                    for i in range(1,df.shape[1]):
                        if list_impacts[k]=='+':
                            ideal_best.append(df.iloc[:,i].max())
                            ideal_worst.append(df.iloc[:,i].min())
                        else:
                            ideal_best.append(df.iloc[:,i].min())
                            ideal_worst.append(df.iloc[:,i].max())
                        k=k+1
            
            
            
            #Calculate eucledian Distance
                    list_splus=[]
                    list_sminus=[]
                    list_temp1=[]
                    list_temp2=[]
                    k=0
                    for i in range(df.shape[0] ):
                        for j in range(1,df.shape[1]):
                            Addinglist_temp1.append((df.iloc[i,j]-ideal_best[k])**2)
                            list_temp2.append((df.iloc[i,j]-ideal_worst[k])**2)
                            k+=1
                        k=0
                        list_splus.append(np.sqrt(sum(list_temp1)))
                        list_sminus.append(np.sqrt(sum(list_temp2)))
                        list_temp1.clear()
                        list_temp2.clear()
            
            
            #Calculate Performance Score
                    performanceScore=[]
                    for i in range(len(list_splus)):
                        performanceScore.append(list_sminus[i]/(list_splus[i]+list_sminus[i]))
            
            
            #Calculate Rank
                    rank_list=[]
                    rank_list=ss.rankdata([-1 * i for i in performanceScore ]).astype(int)
            
            #Adding rank and topsis score to dataframe
                    df=df.assign(Topsis_score=performanceScore,Rank=rank_list)
                    df.to_csv(sys.argv[4],index=False)
                    else:
                        print("no. of columns and no of weights and no of impacts passed should match")
                        exit(0)
        except FileNotFoundError:
            print ("file not found")

if __name__ == "__main__":
    Topsis()
