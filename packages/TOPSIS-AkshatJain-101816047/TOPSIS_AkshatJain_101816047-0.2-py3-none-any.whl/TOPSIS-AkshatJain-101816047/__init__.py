#Importing the libraries
import sys
import pandas as pd
import os
import math
import logging
def root_mean_square(df,collen):
    # Calculating Root Mean Square Value for the Dataframe columns
    rms = []
    for i in range(1,collen):
        a = 0
        for j in range(0,collen):
            a = a + float(df.iloc[j,i])**2
        rms.append(math.sqrt(a))
    return rms

def normalised_decision_matrix(df,collen,rms):
    #Applying the rms value of the column to the column entries
    npv = df.copy()

    for i in range(1,collen):
        for j in range(0,collen):
            npv.iloc[j,i] = npv.iloc[j,i] /rms[i-1]
    return npv

def weight_assignment(npv,w,collen):
    # Multiplying each entry with their weights for making a weighted normalized decison matrix
    for i in range(1,collen):
        for j in range(0,collen):
            npv.iloc[j,i] = npv.iloc[j,i] * float(w[i-1])
    return npv


def ideal_values(npv,collen,imp):
    # Calculating the ideal best and ideal wort value
    vp =[]
    vn = []
    for i in range(1,collen):
        m = []
        for j in range(0,collen):
            m.append(npv.iloc[j,i])
        if imp[i-1]=='+':
            vp.append(max(m))
            vn.append(min(m))
        else:
            vp.append(min(m))
            vn.append(max(m))
    return vp,vn

def cal_euclidean_dist(npv,collen,vp,vn):
    #Calculation the euclidean distance for the matrix best and worst values
    sp = []
    sn = []

    for i in range(0,collen):
        a=0
        b=0
        for j in range(1,collen):
            a = a + (npv.iloc[i,j]-vp[j-1])**2
            b =  b + (npv.iloc[i,j]-vn[j-1])**2
        sp.append(math.sqrt(a))
        sn.append(math.sqrt(b))
    return sp,sn

def cal_performance(sp,sn,collen):
    # Calculating the performance score
    p=[]
    for i in range(0,collen):
        a = sp[i] + sn[i]
        p.append(sn[i]/a)
    return p

def main():
    #No of paramters
    parameters = len(sys.argv)
    #Checking Number of Paramters passed is correct
    if not parameters == 5:
        logging.exception("Error!! Wrong number of parameters")
        logging.exception("Minimum 5 paramters are required")
        logging.exception("Usage: python file.py <filename1.csv> <Weights> <Impacts> <resultfile.csv>")
        logging.exception("Example: python topsis.py inputfile.csv “1,1,1,2” “+,+,-,+” result.csv")
        exit(0)
    # Assigning the values of parameters passed to variables
    filename = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    result_path = sys.argv[4]
    #Checking for File Existence
    if not os.path.isfile(filename):
        raise Exception("File %s doesn't exist.Please pass the correct file."%(filename))

    df = pd.read_csv(filename)#Reading the input file
    #Checking if the input file has atleast 3 columns
    if len(df.columns)<3:
            raise Exception("File %s doesn't have enough columns.Please check the file."%(filename))
    
    collen = len(df.columns)

    #Checking if the weights are sperated by ','
    try:
        w = weights.split(',')
    except:
        logging.exception("The weights are not seperated by ','.")
    
    #Checking if the impacts are sperated by ','
    try:
        imp = impacts.split(',')
    except:
        logging.exception("The impacts are not seperated by ','.")
    
    #Checking if the length of columns from 2nd to last and weights and impacts is same
    if (len(w)==len(imp) and len(w)==collen-1 and len(imp)==collen-1):
        pass
    else:
        raise Exception("Length of Weights,Impacts and dataframe columns from 2nd to last are not same")

    #Checking if all the columns from 2nd to last are numeric
    checklist = df.apply(lambda s: pd.to_numeric(s, errors='coerce').notnull().all())
    for i in range(1,collen):
        if checklist[i]:
            pass
        else:
            raise Exception("Column %s doesn't has all numeric values."%(i+1))
    #Checking if the impacts are only "+" or "-" only
    for i in range(len(imp)):
        if imp[i]=="+" or imp[i]=="-":
            pass
        else:
        raise Exception("Impacts have not all the values of '+' or '-' only")
    #Applying the mathematics required for topsis score calculation
    rms = root_mean_square(df,collen)
    normalized_matrix = normalised_decision_matrix(df,collen,rms)
    weight_matrix = weight_assignment(normalized_matrix,w,collen)
    best_list,worst_list = ideal_values(weight_matrix,collen,imp)
    s_plus,s_minus = cal_euclidean_dist(weight_matrix,collen,best_list,worst_list)
    performace_score = cal_performance(s_plus,s_minus,collen)
    #Assigning the Topsis Score
    df['Topsis Score'] = performace_score
    #Ranking the fields in accordance with Topsis Score
    df['Rank'] = df['Topsis Score'].rank(ascending=False)
    #Exporting the dataframe to the result file
    df.to_csv(result_path,index=False)

if __name__ == "__main__":
    main()