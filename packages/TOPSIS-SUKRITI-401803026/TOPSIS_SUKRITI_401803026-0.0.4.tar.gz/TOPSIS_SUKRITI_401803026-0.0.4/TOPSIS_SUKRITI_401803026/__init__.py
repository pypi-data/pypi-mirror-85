import pandas as pd
import os


def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def TOPSIS(file=None,weights=None,impacts=None,res_file=None):

    #to check number of parameters
    if file == None or weights == None or impacts == None or res_file == None:
        print("Incorrect number of parameters entered. Please check and try again")
        exit(0)
    #to check argument type
    try:
        str(file)
    except:
        print("Only string arguments accepted.")


    #to check if file is of .csv type
    if not(file[-4:]=='.csv'):
        print("Please enter a .csv file and try again")
        exit(0)

    #filenotfound error
    if os.path.isfile(file)==False:
        print("File not found in designated path. Please try again")
        exit(0)
    weight = list(weights.split(","))
    impact = list(impacts.split(","))
    if(weight[-1]=='' or impact [-1]==''):
        print("Error in entering weights or impacts. Please check and try again")
        exit(0)
    for i in range(len(weight)):
        if weight[i].__str__().isnumeric() or is_number(weight[i]) or weight[i]==',':
            continue
        else:
            print(weights)
            print("Weights can only be numeric and can only be separated by ',' ")
            exit(0)

    for i in range(len(weight)):
        weight[i] = float(weight[i])

        if impact[i]=='+' or impact[i]=='-' or impact[i]==',':
            continue
        else:
            print("Impacts can only be '+' or '-' and can only be separated by ',' ")
            exit(0)
    df=pd.read_csv(file)
    result=pd.read_csv(file)
    df.set_index(df.columns[0], inplace=True)
    #checking columns
    if len(df.columns)<3:
        print("The file entered must have ATLEAST 3 columns. Please try again.")
        exit(0)
    for i in df.index:
        for col in df.columns:
            if df[col][i].__str__().isnumeric() or is_number(df[col][i]):
                continue
            else:
                print("All evaluative values in the table must be numeric! Please try again.")
                exit(0)
    #to check if number of columns,weights and impacts are same
    if len(df.columns)!=len(weight):
        print("There are",len(df.columns),"columns but",len(weight),"weights are specified.")
        exit(0)
    elif len(weight)!=len(impact):
        print("There are", len(df.columns), "columns but", len(impact), "impacts are specified.")
        exit(0)
    normd=[]; best=[]; worst=[]
    euclidbest=[]; euclidworst=[]; perfscore=[]
    for i in range(len(df.columns)):
        normd.append(0)
        best.append(0)
        worst.append(0)
    for i in range(len(df.index)):
        euclidbest.append(0)
        euclidworst.append(0)
        perfscore.append(0)
    i=0
    for col in df.columns[:]:
        for j in df[col]:
            normd[i]=normd[i]+(j*j)
        normd[i]=round(pow(normd[i],0.5),4)
        i=i+1
    i=0
    for col in df.columns[:]:
        for j in df[col]:
            df[col] = df[col].replace([j], (j/normd[i])*(weight[i]/sum(weight)))
        i=i+1
    i=0
    for col in df.columns[:]:
        if impact[i]=='+':
            best[i] = max(df[col])
            worst[i] = min(df[col])
        elif impact[i]=='-':
            best[i] = min(df[col])
            worst[i] = max(df[col])
        i=i+1
    j=0
    for ind in df.index:
        i=0
        for col in df.columns[:]:
            euclidbest[j] += pow((df[col][ind]-best[i]),2)
            euclidworst[j] += pow((df[col][ind] - worst[i]), 2)
            i+=1
        euclidbest[j]=pow(euclidbest[j],0.5)
        euclidworst[j]=pow(euclidworst[j],0.5)
        j+=1
    for j in range(len(df.index)):
        perfscore[j]=euclidworst[j]/(euclidworst[j]+euclidbest[j])
    result['TOPSIS Score']=perfscore
    result['Rank']=result['TOPSIS Score'].rank(method='max',ascending=False)
    result.set_index(result.columns[0],inplace=True)
    result.to_csv(res_file)


