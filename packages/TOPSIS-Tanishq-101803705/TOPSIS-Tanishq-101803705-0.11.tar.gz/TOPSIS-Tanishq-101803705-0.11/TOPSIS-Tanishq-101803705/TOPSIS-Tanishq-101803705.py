import pandas as pd
from sklearn import preprocessing
import numpy as np
import sys

def checkDataFrame(df):
    
    df = df.copy()
    
    df = df.T.iloc[1:].T
    
    if(not pd.to_numeric(df['column'], errors='coerce').notnull().all()):
        print('All values in dataset from 2nd column to last column must be numeric')
        return False
    
    return True

def checkString(string, size, category):
    
    
    string = pd.Series(string.split(','))
    if(len(string) != size):
        
        
        # Improve statement to make it more specific
        print(f'Error, {category}s not in proper format or wrong number of values given. All the values must be separated by \',\'\nExample: 1,2,3,4')
        print(string)
        return False
    
    if(category == 'weight'):
        
        if(not string.apply(str.isnumeric).all()):
            
            print('Weights must all be numeric')
            return False
        
    if(category == 'impact'):
        for x in string:
            if x not in ['+', '-']:
                
                print('impacts must be either + or -')
                return False
    return True

def checkArguments():
    
    # print(sys.argv)
    
    if(len(sys.argv) < 2):
        print('Please give one input file.')
        return False
    
    if(len(sys.argv) < 5):
        print('Please give 4 parameters in the following form:\n(input_file, weights, impacts, result_file_name')
        return False
    
    if(len(sys.argv) >5):
        print('Ignoring extra parameters')
        
    
    
    
    return True
    
def checkInputFile():
    
    
    # Check Exists
    inputDF = None
    try:
        inputDF = pd.read_csv(sys.argv[1])
        
    except FileNotFoundError:
        print(f'Error, file \'{sys.argv[1]}\' does not exist.')
        return False
    except:
        print(' Error, file format not correct.')
        return False
    
    # Check Format
    if(inputDF.shape[1] < 3):
        print('Atleast 3 columns required in input file.')
        return False
    
    return True


def finalTopsis(dfin, weights, impacts):
    
    
    L = [dfin.T.values[0]]
    columns = dfin.columns
    df = dfin.T.iloc[1:].T.copy()
    #Normalize data
    
    x = df.values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    df = pd.DataFrame(x_scaled)
    
    
    
    # Weight Assignment
    
    
    total = sum(weights)
    for i in range(0, df.shape[1]):
        
        name = df.iloc[:,i].name
        df[name] = df.iloc[:,i].apply(lambda x: x* weights[i]/total)
         
        
        
        
    
    # Find Ideal best and Ideal worst
    
    newdf = pd.DataFrame(columns = ['best', 'worst'])
    # print(df.shape)
    
    for i in range(0, df.shape[1]):
        
        if(impacts[i] == '+'):
            
            newdf = newdf.append(pd.DataFrame({'best':[max(df.iloc[:,i])],'worst': [min(df.iloc[:,i])]} ))
            
            
        else:
            newdf = newdf.append(pd.DataFrame({'best': [min(df.iloc[:,i])], 'worst': [max(df.iloc[:,i])]} ))
            
    newdf.index = range(len(newdf))
    # Calculating final distance
    dffinal = pd.DataFrame(columns = ['Si+', 'Si-', 'sum', 'performance'])
    
    
    performance = pd.Series(dtype=np.float64)
    for i in range(len(df)):
        sumBest = 0
        sumWorst = 0
        
        
        
        for j in range(df.shape[1]):
            sumBest += (df[j][i] - newdf['best'][j])**2
            sumWorst += (df[j][i] - newdf['worst'][j])**2
            
        sip = sumBest ** 0.5
        sim = sumWorst ** 0.5
        total = sip + sim
        performance = performance.append(pd.Series(sim/total, dtype=np.float64), ignore_index = True)
    dfin['Topsis Score'] = performance
    dfin['Rank'] = performance.rank(ascending=False)
        
    return dfin
    
def outputFile(df):
    
    df.to_csv(sys.argv[4], index=False, header=True)
              
    
    
    # L.extend(df.T.values)
    # df = pd.DataFrame(L).T
    # df.columns = columns
    

# print(sys.argv)
def calculateTopsis():
    pass


if __name__ == '__main__':
    if(not checkArguments(True)):
        sys.exit(0)
    if(not checkInputFile(True)):
        sys.exit(0)
    
    inputDF = pd.read_csv(sys.argv[1])
    
    if(not (checkString(sys.argv[2], inputDF.shape[1] - 1, 'weight') or checkString(sys.argv[3], inputDF.shape[1], 'impact'))):
        sys.exit(0)
    
    outputDF = finalTopsis(inputDF, pd.Series(sys.argv[2].split(',')).astype(int), pd.Series(sys.argv[3].split(',')))
    
    outputFile(outputDF)
