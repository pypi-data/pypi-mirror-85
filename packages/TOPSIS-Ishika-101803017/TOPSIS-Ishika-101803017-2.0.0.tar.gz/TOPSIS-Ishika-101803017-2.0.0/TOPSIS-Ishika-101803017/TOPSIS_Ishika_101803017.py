import numpy as np
import pandas as pd
# import sys
# import os.path

def topsis(inputfile,weights,impacts,result):

    # inputfile=sys.argv[1]
    # weights=sys.argv[2]
    # impacts=sys.argv[3]
    # result=sys.argv[4]
    
    # if len(sys.argv)!=5 :
    #     raise Exception("Exactly 4 arguments are allowed")
    
    # if os.path.exists(inputfile):
    #     pass
    # else:
    #     raise Exception("File is not there!")
    
    if inputfile.endswith(('.csv')):
        pass
    else:
        raise Exception("File should be of csv type")
    
    weights=weights.split(",")
    for i in range(len(weights)):
        weights[i]=int(weights[i])
    
    impacts=impacts.split(",")
    
    file=pd.read_csv(inputfile)
    
    NoOfFeatures=len(file)
    
    if NoOfFeatures<3:
        raise Exception("Atleast 3 columns needed")
    
    if(len(weights)!=NoOfFeatures-1):
        raise Exception("Weights and Column Length dont match")
        
    if(len(impacts)!=NoOfFeatures-1):
        raise Exception("Impacts and Column Length dont match")
    
    RootOfSumOfSquares=[]
    
    for i in range(1,NoOfFeatures):
        L = file.iloc[:,i]
        sum=0
        for j in L:
            if type(j)!=int:
                try:
                    test=int(j)
                except:
                    raise Exception("Non Numeric Value Found!..Cant calculate TOPSIS")
            sum+=(j*j)
        sum=np.sqrt(sum)
        RootOfSumOfSquares.append(sum)
    
    # print(file)
    for i in range(1,NoOfFeatures):
        #L = file.iloc[:,i]
        sum=RootOfSumOfSquares[i-1]
        #sum=L[i-1]
        w=weights[i-1]
        for j in range(len(L)):
            file.iloc[j,i]=(file.iloc[j,i]/sum)*w
            
    # print("div done")
    # print(file)
    
    Vplus=[]
    Vminus=[]
    for i in range(1,NoOfFeatures):
        if impacts[i-1]=='+':
            Vplus.append(max(file.iloc[:,i]))
            Vminus.append(min(file.iloc[:,i]))
        elif impacts[i-1]=='-':
            Vplus.append(min(file.iloc[:,i]))
            Vminus.append(max(file.iloc[:,i]))
        else:
            raise Exception("impacts not correct(should be + or - only)")
            
    Splus=[]
    Sminus=[]
    
    for i in range(file.shape[0]):#iterate per row
        plus=0
        minus=0
        for j in range(1,NoOfFeatures):
            plus+=((Vplus[j-1]-file.iloc[i,j])*(Vplus[j-1]-file.iloc[i,j]))
            minus+=((Vminus[j-1]-file.iloc[i,j])*(Vminus[j-1]-file.iloc[i,j]))
        Splus.append(np.sqrt(plus))
        Sminus.append(np.sqrt(minus))
    
    TopsisScore=[]
    for i in range(file.shape[0]):
        TopsisScore.append(Sminus[i]/(Sminus[i]+Splus[i]))
        
    file['TOPSISScore']=TopsisScore
    # print(file)
    
    copyfile=pd.DataFrame(file)
    # print(copyfile)
    
    copyfile.sort_values(by=['TOPSISScore'],ascending=False,inplace=True)
    
    dictionary={}
    
    rank=1
    for i in range(file.shape[0]):
        dictionary[copyfile.iloc[i,0]]=rank
        rank+=1
        
    ranks=[]
    for i in range(file.shape[0]):
        ranks.append(dictionary[file.iloc[i,0]])
        
    file['Rank']=ranks
    
    # print(file)
    
    file.to_csv (result, index = False, header=True)

# if __name__ == '__main__':
    # main()