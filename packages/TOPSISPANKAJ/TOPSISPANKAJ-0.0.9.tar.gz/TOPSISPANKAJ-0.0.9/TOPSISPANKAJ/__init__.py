import pandas as pd
def topsis(df,weights,impacts):
    df1=pd.DataFrames(columns=df.columns)
    df1=df.copy()
    vjp=[]
    vjn=[]
    r=df.shape[0]
    c=df.shape[1]
    for i in range(1,c):
        df.iloc[:,i]=pd.to_numeric(df.iloc[:,i])
        s=sum(df.iloc[:,i]**2)**0.5
        for j in range(r):
            df.iloc[j,i]=round(df.iloc[j,i]/s,4)
    for i in range(1,c):
        df.iloc[:,i]=round(df.iloc[:,i]*weights[i-1],4)   
    for i in range(1,c):
        if impacts[i-1]=='+':
            vjp.append(max(df.iloc[:,i]))
            vjn.append(min(df.iloc[:,i]))
        else:
            vjn.append(max(df.iloc[:,i]))
            vjp.append(min(df.iloc[:,i]))
    for i in range(r):
        df.loc[i,'sj+']=sum((df.iloc[i,1:c]-vjp)**2)**0.5
    for i in range(r):
        df.loc[i,'sj-']=sum((df.iloc[i,1:c]-vjn)**2)**0.5
# print(df)
    df1['Topsis Score']=round(df['sj-']/(df['sj+']+df['sj-']),2)
    df1['Rank']=df1['Topsis Score'].rank(ascending=False).astype('int')
    return df1