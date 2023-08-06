import sys,csv,pandas as pd, logging as lg

def topsis(input_file, input_weights,input_impacts,resultFile):
    try:
        weights=list(map(int, input_weights.split(',')))
    except ValueError:
        lg.warning("Weights need to be separated by commas.")
        return
    try:    
        impacts=list(input_impacts.split(','))
    except ValueError:
        lg.warning("Impacts need to be separated by commas.")
        return
    try:
        df=pd.read_csv(input_file)
    except:
        lg.warning("Given input file could not be found.")
        return

    for i in impacts:
        if i!='+' and i!='-':
            lg.warning("impacts should be either '+' or '-'.")
            return
    if len(weights)!=len(impacts):
        lg.warning("Number of weights and impacts need to be same.")
        return
    
    if len(df.columns)<3:
        lg.warning("The input model should have atleast 3 attributes.")
        return
    if (len(df.columns)-1) != len(weights):
        lg.warning("Number of weights and attributes are diiferent.")
        return
    for i in df.dtypes[1:]:
        if i!="float64":
            lg.warning("Input file contains non numeric values. Please try again.")
            return
 
   
    rootsum_sq=[]
    for i in df.columns[1:]:  #retrieves the name of columns in df
        total=0
        for j in list(df[i]): #makes list for contents of different columns
            total+=(j**2)   #squaring and ading every element of particular columns 
        rootsum_sq.append(total**(0.5)) #Taking sq root of summed squared elements

    for index,i in enumerate(df.columns[1:]):
        for j in df[i]:
            df[i]=df[i].replace(j,j*weights[index]/rootsum_sq[index]) #multiplying every elements of the columns with weights and dividing by respective rootsum 


    ideal_vals=[]
    for index,i in enumerate(df.columns[1:]): #for every column name or column we find the ideal best and ideal worst values respectively
        if impacts[index]=='-':
            ideal_best=min(df[i])
            ideal_worst=max(df[i])
        else:
            ideal_best=max(df[i])
            ideal_worst=min(df[i])

        ideal_vals.append((ideal_best, ideal_worst))
    
    n = len(df[df.columns[1]]) #number of rows


    performance_score=[]
    for i in range(n):
        totalplus=0
        totalminus=0
        for index,j in enumerate(list(df.iloc[i])[1:]):
            totalplus+=((j-ideal_vals[index][0])**2)
            totalminus+=((j-ideal_vals[index][1])**2)
      
        performance_score.append(totalminus/totalplus+totalminus) #appending performance score for respective rows or attributes

    solution=pd.read_csv(input_file)
    solution['Topsis Score']=performance_score #Adding new column to the df
    solution["Rank"]=solution["Topsis Score"].rank(ascending=False) #Adding rank column to the df
    
    for i in solution["Rank"]:
        i = int(i)

    
    solution.to_csv(f"{resultFile}.csv",index=False)
    print(solution)
    print("Csv file saved successfully at the working directory!")