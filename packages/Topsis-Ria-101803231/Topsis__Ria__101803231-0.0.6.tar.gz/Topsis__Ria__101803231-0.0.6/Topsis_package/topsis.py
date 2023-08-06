import pandas
def topsis(inputname,Weight,Impact,outputname):
    try:
        s=open(inputname)
    except:
        raise Exception("Wrong file or file path")
    df=pandas.read_csv(inputname)
    df2=pandas.read_csv(inputname)
    if(len(df.columns)<2):
        raise Exception('file contains less than 3 columns')
    df1=df.dtypes
    if(list(df1).count('float64')==df.shape[1]):
        raise Exception('enter only numeric values')
    weight=[]
    for i in Weight.replace('"','').split(','):
        weight.append(int(i))
    if(len(df.columns[1:])!=len(weight)):
        raise Exception('the length of weight is not equal to number of columns')
    impact=[]
    for i in Impact.replace('"','').split(','):
        impact.append(i)
    if(len(df.columns[1:])!=len(weight)):
        raise Exception('the length of impact is not equal to number of columns')
    for i in impact:
        if(i!='+' and i!='-'):
            raise Exception('the impact should consist of + and -')
    pandas.set_option('mode.chained_assignment', None)
    k=0
    for i in df.columns[1:]:
        sum1=df[i].sum()
        for j in df.index:
            df.loc[j,i]=df.loc[j,i]/sum1
    for i in df.columns[1:]:
        for j in df.index:
            df.loc[j,i]=df.loc[j,i]*weight[k]
        k+=1
    val_plus=[]
    val_minus=[]
    k=0
    for i in df.columns[1:]:
        if(impact[k]=='+'):
            val_plus.append(df[i].max())
            val_minus.append(df[i].min())
        else:
            val_minus.append(df[i].max())
            val_plus.append(df[i].min())
        k+=1
    s_plus=[]
    s_minus=[]
    k=0
    for i in df.index:
        temp1=0
        temp2=0
        k=0
        for j in df.columns[1:]:
            temp1+=(df[j][i]-val_plus[k])**2
            temp2+=(df[j][i]-val_minus[k])**2
            k+=1
        s_plus.append(temp1**0.5)
        s_minus.append(temp2**0.5)
    perf=[]
    for i in range(len(df.index)):
        perf.append(s_minus[i]/(s_minus[i]+s_plus[i]))
    df2['Topsis score']=perf
    list1=list(sorted(perf,reverse=True).index(x)+1 for x in perf)
    df2['Rank']=list1
    df2.to_csv(outputname, index=False)
