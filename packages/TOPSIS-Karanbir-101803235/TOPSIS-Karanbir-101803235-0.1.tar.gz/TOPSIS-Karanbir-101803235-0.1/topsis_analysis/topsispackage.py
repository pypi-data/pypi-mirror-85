def topsis(inputname,w,im,outputname):
    import pandas as pd
    import sys
    import os
    def is_numeric1(t):
        try:
            t=float(t)
            if (isinstance(t, int)==True or isinstance(t, float)==True):
                return True
        except:
            print("Not a numeric value in columns 2nd and above!")
            sys.exit(0)
        return False
    if os.path.exists(inputname) == False:   ##checking of the file exists
        print("No such file exists")
        sys.exit(0)
    a=[inputname,outputname]
    for val1 in a:  ##correct file type should be passed
        nametemp=val1.split('.')
        if nametemp[1]!="csv":
            print("Only .csv files allowed")
            sys.exit(0)
    df1=pd.read_csv(inputname) 
    df=pd.read_csv(inputname)    ##reading the data frame   
    if df.shape[1]<=3: ## every csv should have more than 3 columns
        print(" No. columns should be greater than 3! ")
        sys.exit(0)
    
    for i in range(1,df.shape[1]): ##checking if all the columns fron 2nd have numeric vallues
        for j in range(df.shape[0]):
            if(is_numeric1(df.iloc[j,i]))==False:
                print(df.iloc[j,i])
                print("All the values in 2nd column and further should be numeric")
                sys.exit(0)
    impact1=im
    totalweight=0.00
    weight1=w
    impacts=impact1.split(',') ##if they will be separated by commas then length will be equal to number of columns
    weights=weight1.split(',') ##if they will be separated by commas then length will be equal to number of columns
    for i in range(len(weights)):
        totalweight=totalweight+float(weights[i])
    if df.shape[1]-1 != len(impacts) or df.shape[1]-1 != len(weights )or len(impacts)!= len(weights):
        print("Either the impacts or weights are not equal to number of columns(starting from 2nd) or the impacts or weights are not separated by commas!")
        sys.exit(0)
    for i in impacts:  ##Impacts must be either +ve or -ve.
        if i not in ["+","-"]:
            print("Impacts should be either + or -!")
            sys.exit(0)
    
    ##vector normalization
    xsquares=[0]*(df.shape[1])
    for i in range(1,df.shape[1]):
        for j in range(df.shape[0]):
            xsquares[i]=xsquares[i]+(df.iloc[j,i])*(df.iloc[j,i])
    for i in range(1,df.shape[1]):
        xsquares[i]=(xsquares[i])**0.5
    for i in range(1,df.shape[1]):
        for j in range(df.shape[0]):
            df.iloc[j,i]=(df.iloc[j,i])/xsquares[i]
    ##weight assignment
    for i in range(1,df.shape[1]):
        for j in range(df.shape[0]):
            df.iloc[j,i]=(df.iloc[j,i])*(float(weights[i-1]))/totalweight
    
    #finding ideal best and ideal best
    ##vjplus is ideal best and vjminus is ideal worst
    vjplus=[0]*(df.shape[1])
    vjminus=[0]*(df.shape[1])
    for i in range(1,df.shape[1]):
        if impacts[i-1]=="+":
                vjplus[i]=max(df.iloc[:,i])
                vjminus[i]=min(df.iloc[:,i])
        elif impacts[i-1]=="-":
                vjplus[i]=min(df.iloc[:,i])
                vjminus[i]=max(df.iloc[:,i])
    
    ##calculating euclidean distance and performace matrix
    siplus=[0]*(df.shape[0])
    siminus=[0]*(df.shape[0])
    si=[0]*(df.shape[0])
    pi=[0]*(df.shape[0])
    for k in range(df.shape[0]):
        for l in range(1,df.shape[1]):
            siplus[k]=siplus[k]+(df.iloc[k,l]-vjplus[l])*(df.iloc[k,l]-vjplus[l])
            siminus[k]=siminus[k]+(df.iloc[k,l]-vjminus[l])*(df.iloc[k,l]-vjminus[l])
    for k in range(df.shape[0]):
        siplus[k]=(siplus[k])**0.5
        siminus[k]=(siminus[k])**0.5
        si[k]=siplus[k]+siminus[k]
        pi[k]=siminus[k]/si[k]
    
    df=df1
    ##now adding the topsis score to dataframe
    df["Topsis Score"]=pi
    ##now ranking according to topsis score
    df["Rank"]=df["Topsis Score"].rank(ascending=False)
    ##making an output file
    df.to_csv(outputname,index=False)
    print("Output generated successfully")
    print(df)
