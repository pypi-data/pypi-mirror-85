def perform_Topsis(source, weights, impacts, result):

    import sys
    import os

    if (os.path.exists(source) == False):
        print('\nFile ', source, ' does not exist, exiting')
        exit(0)
    
    if (os.path.exists(result) == True):
        print('\nFile ', result, ' file already exists, overwrite (y/n) ?')
        ans = input()
        if(ans.lower()=='n'):
            print('\nExiting....')
            exit(0)
        elif(not ans.lower()=='y'):
            print('\nWrong input, Exiting....')
            exit(0)

    for i in range(len(weights)):
        try:
            weights[i] = float(weights[i])
        except:    
            print('\nWeights must be numeric, Exiting....')
            exit(0)

    for i in impacts:
        if(i not in ['+','-']):
            print('\nImpacts must be either positive or negative, Exiting....')
            exit(0)
    
    import pandas as pd

    df = pd.read_csv(source)

    if(len(df.columns)<3):
        print('\nMinimum 3 columns required, Exiting....')
        exit(0)

    if(df.isnull().values.any()):
        print('\nNull Value Detected, Exiting....')
        exit(0)

    for i in range(len(df)):
        for j in range(1, len(df.columns)):
            try:
                df.iloc[i, j] = float(df.iloc[i, j])
            except:
                print('\nNot numeric value detected in column number', j+1, ', Exiting....')
                exit(0)
            
    if(len(impacts)!=len(df.columns)-1):
        print('\n',len(df.columns)-1,' impacts were required instead ', len(impacts),' were given, Exiting....')
        exit(0)

    if(len(weights)!=len(df.columns)-1):
        print('\n',len(df.columns)-1,' weights were required instead ', len(weights),' were given, Exiting....')
        exit(0)
    
    print('\nGenerating output file ....')
    
    temp = df.copy()
    temp['Splus'] = 0
    temp['Sminus'] = 0
    ib = []
    iw = []

    for i in range(1, len(temp.columns)-2):
        SQ = (sum(temp.iloc[:,i]**2))**0.5
        temp.iloc[:,i] = ((temp.iloc[:,i]/SQ)*weights[i-1])
        if(impacts[i-1] == '+'):
            ib.append(max(temp.iloc[:,i]))
            iw.append(min(temp.iloc[:,i]))
        else:
            ib.append(min(temp.iloc[:,i]))
            iw.append(max(temp.iloc[:,i]))

    for i in range(len(temp)):
        temp.iloc[i, len(temp.columns)-2] = ((sum((temp.iloc[i,1:len(temp.columns)-2]-ib)**2))**0.5)
        temp.iloc[i, len(temp.columns)-1] = ((sum((temp.iloc[i,1:len(temp.columns)-2]-iw)**2))**0.5)

    df['Topsis Score'] = 0
    df['Rank'] = 0

    for i in range(len(temp)):
        SUM = temp.iloc[i, len(temp.columns)-1] + temp.iloc[i, len(temp.columns)-2] 
        df.iloc[i, len(temp.columns)-2] = temp.iloc[i, len(temp.columns)-1]/SUM

    df['Rank'] = df['Topsis Score'].rank(ascending = False, method='dense')

    df.to_csv(result, index = False)

    print('\nOutput file generated.')