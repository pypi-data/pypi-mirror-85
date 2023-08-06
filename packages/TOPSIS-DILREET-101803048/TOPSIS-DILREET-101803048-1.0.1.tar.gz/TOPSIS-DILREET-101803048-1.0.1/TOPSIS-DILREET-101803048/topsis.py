import pandas as pd
import numpy as np
import sys
import math as m

def Topsis(input_file,weights,impacts,result_file_name):

    
    df=input_file[:,1:].astype(dtype='float')
    

    #Finding row and column count
    rows=df.shape[0]
    cols=df.shape[1]
    
    #normalizing matrix to get normalized decision matrix and hence we find the normalised performance value 
    for j in range(0,cols):
        sum_sqs=0
        for i in range(0,rows):
            sum_sqs=sum_sqs+df[i,j]*df[i,j]
        sum_sqs=m.sqrt(sum_sqs)
        for i in range(0,rows):
            df[i,j]=df[i,j]/sum_sqs
    

    #  multi[lying weights with the normalised performance value
    # Hence we get the weighted Normalised Decision Matrix
    for j in range(0,cols):
        for i in range(0,rows):
            df[i,j]=df[i,j]*weights[j]

    
    #calculating vj+ i.e the ideal best and vj- i.e. the ideal worst
    v_positive=[]
    v_negative=[]
    for j in range(0,cols):
        if(impacts[j]=='+'):
            v_positive.append(max(df[:,j]))
            v_negative.append(min(df[:,j]))
        # For negative impacts we take minimum value as the best and maximum value as the worst
        elif(impacts[j]=='-'): 
            v_positive.append(min(df[:,j]))
            v_negative.append(max(df[:,j]))
    
    
    #calculating si+ and si- i.e. the euclidian distance
    s_positive=[]
    s_negative=[]
    for i in range(0,rows):
        s1_temp=0
        s2_temp=0
        for j in range(0,cols):
            s1_temp=s1_temp+(df[i,j]-v_positive[j])*(df[i,j]-v_positive[j])
            s2_temp= s2_temp+(df[i,j]-v_negative[j])*(df[i,j]-v_negative[j])
        s_positive.append(m.sqrt(s1_temp))
        s_negative.append(m.sqrt(s2_temp))
    
    
    #calculating topsis score
    performance_score=[]
    for i in range(0,rows):
        performance_score.append( s_negative[i]/(s_negative[i]+s_positive[i]))
    
    #copying performance_score
    performance_score_copy=performance_score.copy() 
    
    #calculating rank
    rank=[]
    for i in range(0,rows):
        rank.append(0);
    t=1;
    for i in range(0,rows):
        d=performance_score_copy.index(max(performance_score_copy)) 
        performance_score_copy[d]=-1
        rank[d]=t
        t=t+1
    
    print(rank)
    
    input_file=pd.DataFrame(input_file)
    input_file['performance score']=performance_score
    
    input_file['rank as per topsis']=rank
    input_file.to_csv(result_file_name)    


def main():
    print(sys.argv)

    if len(sys.argv) != 5:
        print ("Error !! Wrong number of parameters")
        print ("Four parameters are required")
        exit(0)

    if len(sys.argv) == 1:
        print ("File Not Found")
        exit(0)

    input_file= pd.read_csv(sys.argv[1]).values
    
    # if len(input_file)<=2:
    #     print('Input file should contain 3 or more columns '+ sys.argv[1])
    #     sys.exit()

    weights = sys.argv[2]
    impacts = sys.argv[3]

    try:
        weights = list(map(float ,weights.split(',')))
        impacts = list(map(str ,impacts.split(','))) 
    except:
        print('Weights or Impacts are not provided in proper format ')
        sys.exit()
    
    if(len(weights)!=np.size(input_file,1)-1):
        raise Exception('number of weights does not match number of columns')
    
    if(len(impacts)!=np.size(input_file,1)-1):
        raise Exception('number of impacts does not match number of columns')

    
    for each in impacts :
        if each not in ('+','-'):
            print('Impacts are not provided in proper format ')
            sys.exit()

    result_file_name= sys.argv[4]

    Topsis(input_file,weights,impacts,result_file_name)

if __name__=="__main__":
     main()