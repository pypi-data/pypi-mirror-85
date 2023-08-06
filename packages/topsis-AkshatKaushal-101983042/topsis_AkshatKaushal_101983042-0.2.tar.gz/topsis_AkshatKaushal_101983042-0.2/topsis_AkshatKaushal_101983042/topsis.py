import pandas as pd 
import numpy as np
import sys

def normalized_matrix(filename):
    '''To normalize each of the values in the csv file'''
    try:
        dataset = pd.read_csv(filename) #loading the csv file into dataset
        if(len(dataset.axes[1])<3):
            print("Number of columns should be greater than 3")
            sys.exit(1)
            
        attributes = dataset.iloc[:,1:].values #keeping the attributes of the dataset in a different varaiable 
        alternatives = dataset.iloc[:,0].values
        '''the attributes and alternatives are 2-D numpy arrays'''
        sum_cols=[0]*len(attributes[0]) #1-D array with size equal to the nummber of columns in the attributes array
        for i in range(len(attributes)):
            for j in range(len(attributes[i])):
                sum_cols[j]+=np.square(attributes[i][j])
        for i in range(len(sum_cols)):
            sum_cols[i]=np.sqrt(sum_cols[i])    
        for i in range(len(attributes)):
            for j in range(len(attributes[i])):
                attributes[i][j]=attributes[i][j]/sum_cols[j]
        return (attributes,alternatives)
    except Exception as e:
        print("Exception--->",e)

def weighted_matrix(attributes,weights):
    ''' To multiply each of the values in the attributes array with the corresponding weights of the particular attribute'''
    try:
        weights=weights.split(',')
        for i in range(len(weights)):
            weights[i]=float(weights[i])
        weighted_attributes=[]
        for i in range(len(attributes)):
            temp=[]
            for j in range(len(attributes[i])):
                temp.append(attributes[i][j]*weights[j])
            weighted_attributes.append(temp)
        return(weighted_attributes)
    except Exception as e:
        print("Exception--->",e)

def impact_matrix(weighted_attributes,impacts):
    try:
        impacts=impacts.split(',')
        Vjpositive=[]
        Vjnegative=[]
        for i in range(len(weighted_attributes[0])):
            Vjpositive.append(weighted_attributes[0][i])
            Vjnegative.append(weighted_attributes[0][i])
        for i in range(1,len(weighted_attributes)):
            for j in range(len(weighted_attributes[i])):
                if impacts[j]=='+':
                    if weighted_attributes[i][j]>Vjpositive[j]:
                        Vjpositive[j]=weighted_attributes[i][j]
                    elif weighted_attributes[i][j]<Vjnegative[j]:
                        Vjnegative[j]=weighted_attributes[i][j]
                elif impacts[j]=='-':
                    if weighted_attributes[i][j]<Vjpositive[j]:
                        Vjpositive[j]=weighted_attributes[i][j]
                    elif weighted_attributes[i][j]>Vjnegative[j]:
                        Vjnegative[j]=weighted_attributes[i][j]
        Sjpositive=[0]*len(weighted_attributes)
        Sjnegative=[0]*len(weighted_attributes)
        for i in range(len(weighted_attributes)):
            for j in range(len(weighted_attributes[i])):
                Sjpositive[i]+=np.square(weighted_attributes[i][j]-Vjpositive[j])
                Sjnegative[i]+=np.square(weighted_attributes[i][j]-Vjnegative[j])
        for i in range(len(Sjpositive)):
            Sjpositive[i]=np.sqrt(Sjpositive[i])
            Sjnegative[i]=np.sqrt(Sjnegative[i])
        Performance_score=[0]*len(weighted_attributes)
        for i in range(len(weighted_attributes)):
            Performance_score[i]=Sjnegative[i]/(Sjnegative[i]+Sjpositive[i])
        return(Performance_score)
    except Exception as e:
        print("Exception--->",e)

def main():
    try:
        arguments = sys.argv[1:]
        if len(arguments) != 4:
            print("Usage: python topsis.py <InputDataFile> <Weights> <Impacts> <result file name>")
            sys.exit(1)
        (a,b)=normalized_matrix(sys.argv[1])
        c = weighted_matrix(a,sys.argv[2])
        d = impact_matrix(c,sys.argv[3])
        dataset = pd.read_csv(sys.argv[1])
        dataset['topsis score']=""
        dataset['topsis score']=d
        copi=d.copy()
        copi.sort(reverse=True)
        rank=[]
        for i in range(0,len(d)):
            temp=d[i]
            for j in range(0,len(copi)):
                if temp==copi[j]:
                    rank.append(j+1)
                    break
        dataset['Rank']=""
        dataset['Rank']=rank
        dataset.to_csv(sys.argv[4],index=False)   
    except Exception as e:
        print("Exception in main--->",e)
    
if __name__ == '__main__':
    main()
