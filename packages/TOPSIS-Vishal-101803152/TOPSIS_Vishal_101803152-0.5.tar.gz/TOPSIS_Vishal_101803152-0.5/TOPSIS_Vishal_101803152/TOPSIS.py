class Class1:
    import pandas as pd
    import  numpy as np
    import sys
    import math as m

    def main():

        if len(sys.argv) < 5:
            print('Wrong Number of Parameters entered')
            sys.exit()

        file=sys.argv[1]
        weights = sys.argv[2]
        impacts = sys.argv[3]
        result = sys.argv[4]

        try:
            weights = list(map(float ,weights.split(',')))
            impacts = list(map(str ,impacts.split(','))) 
        except:
            print('Weights or Impacts are not provided in proper format ')
            sys.exit()
            
        for each in impacts :
            if each not in ('+','-'):
                print('Impacts are not provided in proper format ')
                sys.exit()

        try:
            input_data = pd.read_csv(file)
        
        except:
            print(file+' File not found')
            sys.exit()
            
        if len(list(input_data.columns))<=2:
            print('Input file should contain three or more than three columns '+ file)
            sys.exit()
            
        data=input_data.iloc[ :,1:]
        (rows,cols)=data.shape
        data=data.values.astype(float)
        sum_of_weights=np.sum(weights)

        if len(weights) != cols:
            print("Number of weights are sparse")
            sys.exit()
            
        if len(impacts) != cols:
            print("Number of impacts are sparse")
            sys.exit()

        for i in range(cols):
            weights[i]/=sum_of_weights


        a=[0]*(cols)

        for i in range(0,rows):
            for j in range(0,cols):
                a[j]+=(data[i][j]*data[i][j])

        for j in range(cols):
            a[j]=m.sqrt(a[j])
            
            
        for i in range(rows):
            for j in range(cols):
                data[i][j]/=a[j]
                data[i][j]*=weights[j]

    
        ideal_best=np.amax(data,axis=0) 
        ideal_worst=np.amin(data,axis=0) 
        for i in range(len(impacts)):
            if(impacts[i]=='-'):         
                temp=ideal_best[i]
                ideal_best[i]=ideal_worst[i]
                ideal_worst[i]=temp

        dist_pos=list()
        dist_neg=list()

        for i in range(rows):
            sq_sum=0
            for j in range(cols):
                sq_sum+=pow((data[i][j]-ideal_best[j]), 2)

            dist_pos.append(float(pow(sq_sum,0.5)))


        for i in range(rows):
            sq_sum=0
            for j in range(cols):
                sq_sum+=pow((data[i][j]-ideal_worst[j]), 2)

            dist_neg.append(float(pow(sq_sum,0.5)))


        performance_score=dict()

        for i in range(rows):
            performance_score[i+1]=dist_neg[i]/(dist_neg[i]+dist_pos[i])

        actual=list(performance_score.values())
        sort=sorted(list(performance_score.values()) , reverse=True)

        rank=dict()

        for val in actual:
            rank[(sort.index(val) + 1)] = val
            sort[sort.index(val)] =-sort[sort.index(val)]


        output=input_data
        output['Topsis_score']=list(rank.values())
        output['Rank']=list(rank.keys())


        res=pd.DataFrame(output)
        res.to_csv(result,index=False)

        
if __name__=="__main__": 
    main()