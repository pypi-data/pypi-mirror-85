import sys
import pandas as pd

if len(sys.argv)!=5:
    raise Exception ('Incorrect number of parameters!')
try:
    df = pd.read_csv(sys.argv[1])
    if len(df.columns) < 3:
        raise Exception('Input file must contain three or more columns!')
    
    df1 = df.copy()
    weights = sys.argv[2].split(',')
    impacts = sys.argv[3].split(',')
    
    if len(weights) != (len(df.columns)-1) or len(impacts) != (len(df.columns)-1):
        raise Exception('Number of weights,impacts and columns are not same!')
    
    def find_rss(col):
        temp = 0
        for i in col:
            temp += i**2
        rss = temp**(1/2)
        return rss

    for col in range(1,len(df.columns)):
        rss = find_rss(df.iloc[:,col])
        df.iloc[:,col] = df.iloc[:,col].apply(lambda x:x/rss)
    
    for i in range(0,len(weights)):
        weights[i] = float(weights[i])
    
    for col in range(1,len(df.columns)):
        df.iloc[:,col] = df.iloc[:,col].apply(lambda x:x*weights[col-1])
    
    list1 = ['V+']
    list2 = ['V-']
    
    for col in range(1,len(df.columns)):
        if impacts[col-1]=='+':
            list1.append(df.iloc[:,col].max())
            list2.append(df.iloc[:,col].min())
        else:
            list1.append(df.iloc[:,col].min())
            list2.append(df.iloc[:,col].max())
    
    df = df.append(pd.Series(list1,index=df.columns),ignore_index=True)
    
    df = df.append(pd.Series(list2,index=df.columns),ignore_index=True)
    
    list1 =[]
    list2 =[]
    
    rows = df.shape[0]
    for row in range(0,rows-2):
        s1,s2 = 0,0
        for col in range(1,len(df.columns)):
            s1 = s1+(df.iloc[row,col]-df.iloc[rows-2,col])**2
            s2 = s2+(df.iloc[row,col]-df.iloc[rows-1,col])**2
        list1.append(s1**(1/2))
        list2.append(s2**(1/2))
    
    df.drop([rows-1,rows-2],inplace=True)
    df['S+'] = list1
    df['S-'] = list2
    df['S+ + S-'] = df['S+'] + df['S-']
    df1['Topsis Score'] = df['S-']/df['S+ + S-']
    df1['Rank'] = df1['Topsis Score'].rank(ascending=False)
    df1.to_csv(sys.argv[4],index=False)

except FileNotFoundError:
    print('File not found!')
