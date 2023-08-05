import sys,csv,pandas as pd, logging

def topsis(inp_file, inp_weights,inp_impacts,resultFileName):
    try:
        weights=list(map(int, inp_weights.split(',')))
    except ValueError:
        logging.warning("Please use commas to seperate weights. Weights: "+ inp_weights)
        return
    impacts=list(inp_impacts.split(','))
    try:
        df=pd.read_csv(inp_file)
    except:
        logging.warning("File not found. Please try again. File: " + inp_file)
        return

    for i in impacts:
        if i!='+' and i!='-':
            logging.warning("Impacts contain foriegn values. Please try again with '+' and '-' ONLY. Seperate them using commas ONLY. Impacts: " + impacts)
            return
    if len(weights)!=len(impacts):
        logging.warning("Number of weights and impacts are different. Please try again.")
        return
    
    if len(df.columns)<3:
        logging.warning("There is only one or less Models in input file. Please try again.")
        return
    if (len(df.columns)-1) != len(weights):
        logging.warning("Number of weights and attributes are not the same. Please try again")
        return
    for i in df.dtypes[1:]:
        if i!="float64":
            logging.warning("Input file contains non numeric values. Please try again.")
            return
    #data=[list(i) for i in df[j] for j in df.columns[1:] ]
   
    root_sum_sq=[]
    for i in df.columns[1:]:
        total=0
        for j in list(df[i]):
            total+=(j**2)
        root_sum_sq.append(total**(0.5))
    for index,i in enumerate(df.columns[1:]):
        for j in df[i]:
            df[i]=df[i].replace(j,j*weights[index]/root_sum_sq[index])


    ideal=[]
    for index,i in enumerate(df.columns[1:]):
        if impacts[index]=='-':
            ideal_best=min(df[i])
            ideal_worst=max(df[i])
        else:
            ideal_best=max(df[i])
            ideal_worst=min(df[i])

        ideal.append((ideal_best, ideal_worst))
    
    n=len(df.index)
    tp=[]
    for i in range(n):
        totalplus=0
        totalminus=0
        for index,j in enumerate(list(df.iloc[i])[1:]):
            totalplus+=((j-ideal[index][0])**2)
            totalminus+=((j-ideal[index][1])**2)
      
        tp.append(totalminus/totalplus+totalminus)
    final=pd.read_csv(inp_file)
    final['Topsis Score']=tp
    final["Rank"]=final["Topsis Score"].rank(ascending=False)
    for i in final["Rank"]:
        final["Rank"]=final["Rank"].replace(i,'{:0g}'.format(i))
    print(final)
    final.to_csv(f"{resultFileName}.csv",index=False)
    print("CSV file has been created in your working directory.")

    
