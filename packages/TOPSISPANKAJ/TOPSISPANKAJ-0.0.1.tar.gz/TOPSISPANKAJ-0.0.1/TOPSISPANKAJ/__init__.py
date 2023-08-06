import pandas as pd
def topsis(df,weights,impacts)
    vjp=[]
    vjn=[]
    for i in range(1,df.shape[1]):
        df.iloc[:,i]=pd.to_numeric(df.iloc[:,i])
        s=sum(df.iloc[:,i]**2)**0.5
        for j in range(df.shape[0]):
            df.iloc[j,i]=round(df.iloc[j,i]/s,4)
    for i in range(1,df.shape[1]):
        df.iloc[:,i]=round(df.iloc[:,i]*weights[i-1],4)   
    for i in range(1,df.shape[1]):
        if impacts[i-1]=='+':
            vjp.append(max(df.iloc[:,i]))
            vjn.append(min(df.iloc[:,i]))
        else:
            vjn.append(max(df.iloc[:,i]))
            vjp.append(min(df.iloc[:,i]))
# print(vjp,vjn)
    for i in range(df1.shape[0]):
        df.loc[i,'sj+']=sum((df.iloc[i,1:df1.shape[1]]-vjp)**2)**0.5
    for i in range(df1.shape[0]):
        df.loc[i,'sj-']=sum((df.iloc[i,1:df1.shape[1]]-vjn)**2)**0.5
# print(df)
    df['Topsis Score']=round(df['sj-']/(df['sj+']+df['sj-']),2)
    df['Rank']=df['Topsis Score'].rank(ascending=False).astype('int')
    return df