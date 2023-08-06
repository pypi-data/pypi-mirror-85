import sys
import pandas as pd
import copy

arguments = copy.deepcopy(sys.argv)

if len(sys.argv) != 5:
    raise Exception("Enter four parameters")
if sys.argv[1].endswith('.csv'):
    pass
else:
    raise Exception("Imput file should be of type - .csv")


# make a list of weights
weights = []
for w in arguments[2]:
    if w != ',':
        weights.append(int(w))


# make a list of impacts
impacts = []
for imp in sys.argv[3]:
    if imp == ',':
        pass
    elif imp == '+' or '-':
        impacts.append(imp)

    else:
        raise Exception("Impact must be positive(+) or negative (-)")

# compare length of weights, impacts list
if len(weights) != len(impacts):
    raise Exception("impacts and weights must be of same length")


# Reading input file
df = pd.read_csv(sys.argv[1])
num_of_col = len(df.columns)

# check number of columns in input file
if num_of_col < 3:
    raise Exception("Input file must have atleast 3 columns")

# check length of weights list, and number of numeric columns
if len(impacts) != num_of_col - 1:
    raise Exception("Impacts, weights and number of columns  must be of same length")

#Reading input file
df = pd.read_csv(sys.argv[1])
features=df.columns.tolist()[1:]

temp=df.copy()          #making temp copy of df

for i in range(0,len(features)):
    s=((temp[features[i]]**2).sum())**0.5
    temp[features[i]]=temp[features[i]]/s

for i in range(0, len(features)):
    temp[features[i]]*=int(weights[i])

#Finding ideal best and ideal worst
idealBest=[]
idealWorst=[]
for i in range(0, len(features)):
    if impacts[i]=='+':
        idealBest.append(temp[features[i]].max())
        idealWorst.append(temp[features[i]].min())
    elif impacts[i]=='-':
        idealBest.append(temp[features[i]].min())
        idealWorst.append(temp[features[i]].max())

# Calculating euclidean distance
for i in range(5):
    temp.loc[i, 'Best']=0
    temp.loc[i, 'Worst']=0
    for j in range(0, len(features)):
        temp.loc[i, 'Best']+=((temp.loc[i, features[j]]-idealBest[j])**2)
        temp.loc[i, 'Worst']+=((temp.loc[i, features[j]]-idealWorst[j])**2)
    temp.loc[i, 'Best']=(temp.loc[i, 'Best'])**0.5
    temp.loc[i, 'Worst']=(temp.loc[i, 'Worst'])**0.5

#Calculating topsis score
temp['Score']=temp['Worst']/(temp['Best']+temp['Worst'])
df['Topsis score']=temp['Score']
df["Rank"] = df["Topsis score"].rank(ascending=False)

df.to_csv(arguments[4], index=False, header=True)       #Writing to csv