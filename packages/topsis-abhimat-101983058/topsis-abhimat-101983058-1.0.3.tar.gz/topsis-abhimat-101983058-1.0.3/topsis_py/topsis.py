import numpy as np
from scipy.stats import rankdata
import sys
import os
import pandas as pd

def main():

    if len(sys.argv)!=5:
        print("Incorrect Number of Arguments Passed")
        print("Pass Argument in this format: $python <programName> <dataset> <weights array> <impacts array> <output filename>")
        raise Exception('Pass Proper Arguments')

    if 'csv' not in sys.argv[1].split('.'):
        print(sys.argv[1].split('.'))
        raise Exception('Pass CSV files Only')
    if(pd.read_csv(sys.argv[1]).bool == False):
        raise Exception('File Not Found')
    
    dataset = pd.read_csv(sys.argv[1]).values             
    decisionMatrix = dataset[:,1:]                        
    weights = [int(i) for i in sys.argv[2].split(',')]    
    impacts = sys.argv[3].split(',')                     
    output_file = sys.argv[4]
    print("Data Given")
    print(dataset)
    topsis(decisionMatrix , weights , impacts, output_file, dataset)
    
def topsis(decisionMatrix,weights,impacts):
    r,c = decisionMatrix.shape
    if (c < 3):
        return print("Input file must contain three or more columns which have numerical values")
    if len(weights) != c :
        return print("Number of weights is not equal to number of columns. Note- Weights also must be separated by commas (,)")
    if len(impacts) != c :
        return print("Number of impacts is not equal to number of columns.  Note- Impacts also must be separated by commas (,)")
    if not all(i > 0 for i in weights) :
        return print("Weights must be > 0")
    if not all(i=="+"or i=="-" for i in impacts) :
        return print("Impacts can only be '+' and '-' signs")

    data = np.zeros([r+2,c+4])
    s=sum(weights)
    
    for i in range(c):
        for j in range(r):
            data[j,i] = (decisionMatrix[j,i]/np.sqrt(sum(decisionMatrix[:,i]**2)))*weights[i]/s
    
    for i in range(c):
        data[r,i] = max(data[:r,i])
        data[r+1,i] = min(data[:r,i])
        if impacts[i] == "-":
            data[r,i] , data[r+1,i] = data[r+1,i] , data[r,i]
    
    for i in range(r):
        data[i,c] = np.sqrt(sum((data[r,:c] - data[i,:c])**2))
        data[i,c+1] = np.sqrt(sum((data[r+1,:c] - data[i,:c])**2))
        data[i,c+2] = data[i,c+1]/(data[i,c] + data[i,c+1])
        
    data[:r,c+3] = len(data[:r,c+2]) - rankdata(data[:r,c+2]).astype(int) + 1
    a = []
    a.append(data[:5,c+2].tolist())
    a.append(data[:5,c+3].tolist())
    #dataset_orignal['Score'] = a
    #a = data[:5,c+3].tolist()
    #dataset_orignal['Rank'] = a
    col = ['Corr','Rseq','RMSE','Accuracy']
    df = pd.DataFrame(data = decisionMatrix, columns = col)
    df['Topsis Score'] = a[0]
    df['Rank'] = a[1]
    l = np.arange(1,r+1)
    df.insert(loc = 0, column='Model', value = l)
    return df

if __name__ == "__main__":
    main()