import sys
import time
import pandas as pd
import numpy as np
import math

def main():
    # Argument Check
    # Read the command line arguments
    if len(sys.argv) != 5:
        print ("\nError! Wrong number of parameters")
        print ("5 parameters are required")
        print ("Usages: python topsis.py <InputDataFile> <Weights> <Impacts> <ResultFileName>")
        print ("Example: python topsis.py inputfile.csv “1,1,1,2” “+,+,-,+” result.csv")
        sys.exit(0)
    
    
    # Variables are defined        
    # Command Line Arguments
        
    args = len(sys.argv) - 1
    inputFile = sys.argv[1]
    outputFile = sys.argv[4]

    try:
        weights = list(map(float ,sys.argv[2].split(',')))
        impacts = list(map(str ,sys.argv[3].split(','))) 
    except:
        print('Weights or Impacts are not provided in proper format ')
        sys.exit(0)
        
    for each in impacts :
        if each not in ('+','-'):
            print('Impacts are not provided in proper format ')
            sys.exit(0)

    try:
        input_data = pd.read_csv(inputFile)
    
    except:
        print(inputFile+' File not found');
        sys.exit(0)
        
    if len(list(input_data.columns))<=2:
        print('Input file should contain 3 or more columns '+ file)
        sys.exit()



    # Input File are read through read_csv() functions
    inputTable = pd.read_csv(inputFile)
    weights = [int(i) for i in sys.argv[2].split(',')]
    impacts = sys.argv[3].split(',')
    labels = [i for i in inputTable[1:]]

    # MAIN PROGRAM STARTS HERE

    # Each file is manipulated
    outputTable = inputTable.copy()

    # Add the Topsis Score and Rank column to the output table
    outputTable['Topsis Score'] = [0 for i in range(0,len(inputTable))]
    outputTable['Rank'] = [0 for i in range(0,len(inputTable))]

    sumOfSquares = {labels[i] : 0 for i in range(1,len(labels))}
    newWeights = {labels[i] : 0 for i in range(1,len(labels))}

    # Processing the input table
    for index, row in inputTable.iterrows():
        for i in labels[1:]:
            sumOfSquares[i] += row[i]*row[i]

    for i in sumOfSquares:
        sumOfSquares[i] = math.sqrt(sumOfSquares[i])
    
    # Perform the TOPSIS Normalization operations on the data
    inputTable = outputTable.copy()

    for index, row in outputTable.iterrows():
        for i in labels[1:]:
            inputTable.loc[index,i] = row[i] / sumOfSquares[i]
        
    # Define weights and impact dictionary      
    newWeights = {i:weights[index]/sum(weights) for index,i in enumerate(labels[1:])}
    newImpacts = {i:impacts[index] for index,i in enumerate(labels[1:])}


    for index, row in outputTable.iterrows():
        for i in labels[1:]:
            inputTable.loc[index,i] *= newWeights[i]
        
    v1 = dict()
    v2 = dict()

    for index, row in outputTable.iterrows():
        for i in labels[1:]:
            if newImpacts[i] == '+':
                v1[i] = max(inputTable[i])
                v2[i] = min(inputTable[i])
            elif newImpacts[i] == '-':
                v1[i] = min(inputTable[i])
                v2[i] = max(inputTable[i])
   
    inputTable = inputTable.append(v1,ignore_index=True)
    inputTable = inputTable.append(v2,ignore_index=True)     

    inputTable['S1'] = [0 for i in range(0,len(inputTable))]
    inputTable['S2'] = [0 for i in range(0,len(inputTable))]
    inputTable['S12'] = [0 for i in range(0,len(inputTable))]

    for index, row in inputTable.iterrows():
        if index < len(inputTable) - 2:
            for i in labels[1:]:
                row['S1'] += (float(inputTable.loc[len(inputTable)-2][i]) - float(row[i])) * (float(inputTable.loc[len(inputTable)-2][i]) - float(row[i])) 
                row['S2'] += (float(inputTable.loc[len(inputTable)-1][i]) - float(row[i])) * (float(inputTable.loc[len(inputTable)-1][i]) - float(row[i]))
            row['S1'] = math.sqrt(row['S1'])
            row['S2'] = math.sqrt(row['S2'])
            row['S12'] = row['S1'] + row['S2']
            outputTable.loc[index,'Topsis Score'] = row['S2'] / (row['S1'] + row['S2'])

    rank_values = sorted(outputTable['Topsis Score'], reverse = True)


    for index,row in inputTable.iterrows():
        if index < len(inputTable) - 2:
            outputTable.loc[index,'Rank'] = rank_values.index(outputTable.loc[index]['Topsis Score']) + 1
    

    print('Result:\n')
    print(outputTable)
    
    # Save output file
    outputTable.to_csv(outputFile,index=False)
    print('\nResult File successfully created')

        
        
if __name__ == "__main__":
    main()
    