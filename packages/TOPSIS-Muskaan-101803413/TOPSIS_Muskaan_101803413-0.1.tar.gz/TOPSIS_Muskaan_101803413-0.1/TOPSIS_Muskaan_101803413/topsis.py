# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 15:05:08 2020

@author: muska
"""


import pandas as pd
import sys

def topsis():
    def rankify(A): 
      
        # Rank Vector 
        R = [0 for x in range(len(A))] 
      
        # Sweep through all elements 
        # in A for each element count 
        # the number of less than and  
        # equal elements separately 
        # in r and s. 
        for i in range(len(A)): 
            (r, s) = (1, 1) 
            for j in range(len(A)): 
                if j != i and A[j] > A[i]: 
                    r += 1
                if j != i and A[j] == A[i]: 
                    s += 1       
             
            # Use formula to obtain rank 
            R[i] = r + (s - 1) / 2
      
        # Return Rank Vector 
        return R  
    
    if len(sys.argv)==1 or len(sys.argv)>5:
        print("Error! Wrong number of arguments")
        print("4 parameters are required...")
        exit(0)
    
    arg = sys.argv[1]
    list1 = arg.split('.')
    extension = list1[1]
    if(extension != 'csv'):
        print("Invalid file extension!")
        exit(0)
    
    arg = sys.argv[4]
    list1 = arg.split('.')
    extension = list1[1]
    if(extension != 'csv'):
        print("Invalid file extension!")
        exit(0)
    
    try:
        df = pd.read_csv(sys.argv[1])
        col = df.columns
        if (len(col)<3):
            raise ValueError
        
        for i in range(1,df.shape[1]):
            if df.iloc[:,i].dtype=="float64":
                continue
            else:
                print("Columns should be of numeric type only")
                exit(0)
        
        weights = sys.argv[2].split(',')
        weights = [int(i) for i in weights] 
        if (len(weights) != (len(col)-1)):
            raise ValueError
        
        impacts = sys.argv[3].split(',')
        for i in impacts:
            if i!='+' and i!='-':
                print("Impacts must be either + or -")
                exit(0)
        if (len(impacts) != (len(col)-1)):
            raise ValueError
        
        df_new = df.drop("Model", 1)
        df1 = df_new
        
        for j in range(df1.shape[1]):
            n = sum(df1.iloc[:,j]**2)**0.5
            for i in range(df1.shape[0]):
                df_new.iloc[i,j] = df_new.iloc[i,j]*weights[j]/n
            
        ideal_best = []
        ideal_worst = []
        for i in range(df1.shape[1]):
            if impacts[i]=='+':
                ideal_worst.append(min(df_new.iloc[:,i]))
                ideal_best.append(max(df_new.iloc[:,i]))
            else:
                ideal_worst.append(max(df_new.iloc[:,i]))
                ideal_best.append(min(df_new.iloc[:,i]))
                
        dib=(df_new-ideal_best)**2
        diw=(df_new-ideal_worst)**2
        s_plus = []
        s_minus = []
        for j in range(df1.shape[0]):
        	s_plus.append(sum(dib.iloc[j,:])**0.5)
        	s_minus.append(sum(diw.iloc[j,:])**0.5)
        
        s_total = []
        for i in range(len(s_plus)):
            s_total.append(s_plus[i]+s_minus[i])
            
        p = []
        for i in range(len(s_minus)):
            p.append(s_minus[i]/s_total[i])
        
        df["Topsis Score"] = p
        
        r = rankify(p)
        df["Rank"] = r
    
        df.to_csv(sys.argv[4])      
           
    except ValueError:
        print("Atleast 3 columns should be there in the input file!!")
        print("Number of weights, number of impacts and number of columns must be same")
    except:
        print("Error!! No such file exists")
    
if __name__ == "__main__":
    topsis()