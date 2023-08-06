import sys
import os


class myexception(Exception):
    pass

def decision_matrix(df,weights,impacts):
    # no. of raws in provided file
    m=df.shape[0] 
    # no. of columns in provided file
    n=len(df.columns) 
    

# Normalization
    # find the root of sum of each entries in respective column
    denominator=[0]
    for i in range(1,n):
        temp=0
        for j in df.iloc[:,i]:
            temp=temp+pow(j,2)
        denominator.append(pow(temp,0.50))


    # performance value in each cell
    # divide each element in the datafile by the above considered denominator for each column
    for i in range(1,n):
        count=0
        for j in df.iloc[:,i]:
            df.iloc[count,i]=df.iloc[count,i]/denominator[i]
            count+=1
    
    # changinf weights to float
    for i in range(1,n):
        weights[i-1]=float(weights[i-1])

#  weighted normalised decision matrix        
    # multiply performance value in column with their column respective weights
    for i in range(1,n):
        count=0
        for j in df.iloc[:,i]:
            df.iloc[count,i]=df.iloc[count,i]*weights[i-1]
            count+=1

    # calculate the ideal best and ideal worst values
    Vbest=[0]
    Vworst=[0]
    for i in range(1,n):
        if impacts[i-1]=='+':
            Vbest.append(df.iloc[:,i].max())
            Vworst.append(df.iloc[:,i].min())
        else:
            Vbest.append(df.iloc[:,i].min())
            Vworst.append(df.iloc[:,i].max())

    #find euclidean distances from ideal best and ideal worst values   euclidean distance is denoted as ed
    ed_best=[]
    ed_worst=[]
    for i in range(0,m):
        temp_best=0
        temp_worst=0
        for j in range(1,n):
            temp_best+=pow(df.iloc[i,j]-Vbest[j],2)
            temp_worst+=pow(df.iloc[i,j]-Vworst[j],2)
        ed_best.append(pow(temp_best,0.50))
        ed_worst.append(pow(temp_worst,0.50))

    #calculate performance score
    performance_score=[]
    for i in range(0,m):
        performance_score.append(ed_worst[i]/(ed_worst[i]+ed_best[i]))
    # insert columns topsis score and rank in the dataframe
    df['Topsis Score']=performance_score
    df['Rank'] = df['Topsis Score'].rank(method='max',ascending=False)
    return df

def topsis(inputfilename,weights,impacts,outputfilename):
    
    
    try:
        arguments=[inputfilename,weights,impacts,outputfilename]
        if(len(arguments)!=4):
            raise myexception("Usage: topsis(InputDataFile> <Weights> <Impacts> <OutputFile>)")
        if not inputfilename.endswith('.csv'):
            raise myexception("this is not a valid file format...!!!")
        for i in impacts:
            if i=='+' or i=='-':
                pass
            else:
                raise myexception('impacts must be either positive or negative')
        df=pd.read_csv(inputfilename)
        if not len(df.columns)>=3:
            raise myexception("input file must contains 3 or more columns")
        if len(weights)==len(impacts):
            if len(weights)==(len(df.columns)-1):
                pass
            else:
                raise myexception("length of columns is not same as that of weights")
        else:
            raise myexception("length of weights is not same as that of impacts") 
        df_new=decision_matrix(df,weights,impacts)
        df_new.to_csv(outputfilename)
    except:
        raise myexception("file with the given name does not found")