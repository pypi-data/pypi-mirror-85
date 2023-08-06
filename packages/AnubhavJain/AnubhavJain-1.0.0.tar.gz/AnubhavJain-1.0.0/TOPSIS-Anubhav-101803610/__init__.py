import pandas as pd 
import numpy as np
import sys


def normalized_matrix(filename):
    
    dataset = pd.read_csv(filename) 
    attributes = dataset.iloc[:,1:].values  
    alternatives = dataset.iloc[:,0].values
    
    sum_cols=[0]*len(attributes[0]) 

    for i in range(len(attributes)):
        for j in range(len(attributes[i])):
            sum_cols[j]+=np.square(attributes[i][j])
    
    for i in range(len(sum_cols)):
        sum_cols[i]=np.sqrt(sum_cols[i])    
    
    for i in range(len(attributes)):
        for j in range(len(attributes[i])):
            attributes[i][j]=attributes[i][j]/sum_cols[j]
    
    return (attributes,alternatives)


def weighted_matrix(attributes,weights):
    
    weights=weights.split(',')
    sum_weights=0
    
    for i in range(len(weights)):
        weights[i]=float(weights[i])
        sum_weights+=weights[i]
    
    for i in range(len(weights)):
        weights[i]=weights[i]/sum_weights
    
    weighted_attributes=[]
    
    for i in range(len(attributes)):
        
        temp=[]
        
        for j in range(len(attributes[i])):
            temp.append(attributes[i][j]*weights[j])
        
        weighted_attributes.append(temp)
    
    return(weighted_attributes)


def impact_matrix(weighted_attributes,impacts):
    
    impacts=impacts.split(',')
    
    Vjpositive=[]
    Vjnegative=[]
    
    for i in range(len(weighted_attributes[0])):
        Vjpositive.append(weighted_attributes[0][i])
        Vjnegative.append(weighted_attributes[0][i])
    
    for i in range(1,len(weighted_attributes)):
        for j in range(len(weighted_attributes[i])):
            if impacts[j]=='+':
                if weighted_attributes[i][j]>Vjpositive[j]:
                    Vjpositive[j]=weighted_attributes[i][j]
                elif weighted_attributes[i][j]<Vjnegative[j]:
                    Vjnegative[j]=weighted_attributes[i][j]
            elif impacts[j]=='-':
                if weighted_attributes[i][j]<Vjpositive[j]:
                    Vjpositive[j]=weighted_attributes[i][j]
                elif weighted_attributes[i][j]>Vjnegative[j]:
                    Vjnegative[j]=weighted_attributes[i][j]
    
    Sjpositive=[0]*len(weighted_attributes)
    Sjnegative=[0]*len(weighted_attributes)
    
    for i in range(len(weighted_attributes)):
        for j in range(len(weighted_attributes[i])):
            Sjpositive[i]+=np.square(weighted_attributes[i][j]-Vjpositive[j])
            Sjnegative[i]+=np.square(weighted_attributes[i][j]-Vjnegative[j])
    
    for i in range(len(Sjpositive)):
        Sjpositive[i]=np.sqrt(Sjpositive[i])
        Sjnegative[i]=np.sqrt(Sjnegative[i])
    
    Performance_score=[0]*len(weighted_attributes)
    for i in range(len(weighted_attributes)):
        Performance_score[i]=Sjnegative[i]/(Sjnegative[i]+Sjpositive[i])
    
    return(Performance_score)


def main():
    
    arguments = sys.argv[1:]
    
    if len(arguments) != 4:
        print("Usage: python topsis.py <InputDataFile> <Weights> <Impacts> <ResultFile.csv>")
        sys.exit(1)
    
    a,b=normalized_matrix(sys.argv[1])
    c = weighted_matrix(a,sys.argv[2])
    d = impact_matrix(c,sys.argv[3])
    
    ResultFile = sys.argv[4]
    existingFile = pd.read_csv(sys.argv[1])
    existingFile['Topsis Score'] = d
    existingFile['Rank'] = existingFile['Topsis Score'].rank(ascending = False)
    existingFile.to_csv(ResultFile)
    
    
if __name__ == '__main__':
    main()