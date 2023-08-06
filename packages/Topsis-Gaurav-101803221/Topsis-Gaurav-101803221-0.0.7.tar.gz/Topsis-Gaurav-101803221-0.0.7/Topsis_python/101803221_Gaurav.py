import sys
import pandas
import os
import numpy as np
inputs = list(sys.argv)
if len(inputs)!=5:
    sys.exit('Wrong number of inputs')
inputFile = inputs[1]
if not os.path.exists(inputFile):
    sys.exit('no such file exists ->'+inputFile)
ext = os.path.splitext(inputFile)[1]
if ext not in ['.csv','.txt','.json','.xlsx']:
    sys.ext('wrong input format->'+inputFile)
if ext=='.csv' or ext=='.txt':
    data = pandas.read_csv(inputFile)
elif ext=='.json':
    data = pandas.read_json(inputFile)
else:
    data = pandas.read_xlsx(inputFile)
rows,col = data.shape
if col<3:
    sys.exit('file contains less than 3 columns')


weights = inputs[2]
impacts = inputs[3]
try:
    weights = list(map(int,weights.split(',')))
    impacts = list((impacts.split(',')))
except:
    sys.exit('wrong file -> weights or impacts')
print(weights,impacts)
if len(weights)!=col-1 or len(impacts)!=col-1:
    sys.exit('wrong number of weights or impacts')
columns = list(data.columns[1:])
i = 0
normData = data.drop(data.columns[0],axis=1)
iBest = [0]*(col-1)
iWorst = [0]*(col-1)
while i<col-1:
    current = data[columns[i]]
    try:
        current = current.astype(float)
    except:
        sys.exit('wrong datatype in file')
    # calculating sqrt of sos
    normFactor = (np.square(current).sum())**0.5
    normData[columns[i]] = normData[columns[i]]/normFactor
    #weight multiplication
    normData[columns[i]] = normData[columns[i]]*(weights[i])
    #ideal best/worst
    min1 = min(normData[columns[i]])
    max1 = max(normData[columns[i]])
    if impacts[i]=='+':
        iBest[i] = max1
        iWorst[i] = min1
    elif impacts[i]=='-':
        iBest[i] = min1
        iWorst[i] = max1
    else:
        sys.exit('wrong input->impact')
    i+=1
cost = []
row = 0
while row<rows:
    c = 0
    costb = 0
    costw = 0
    while c<col-1:
        costb += (iBest[c]-normData.iloc[row,c])**2
        costw += (iWorst[c]-normData.iloc[row,c])**2
        c+=1
    splus = costb**0.5
    sminus = costw**0.5
    cost.append(sminus/(splus+sminus))
    print(splus,sminus)
    row+=1
data['Topsis Score'] = cost
data['Rank'] = data['Topsis Score'].rank(method='first',ascending=False)
print(data)
output = inputs[4]
if os.path.splitext(output)[1]=='.csv':
    data.to_csv(output)
    print('file created '+output)
else:
    sys.exit('wrong output file')





    