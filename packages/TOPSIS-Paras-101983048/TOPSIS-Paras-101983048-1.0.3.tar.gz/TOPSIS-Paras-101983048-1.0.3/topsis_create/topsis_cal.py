import pandas as pd
import  numpy as np

def topsis(filename , weights , impacts):

    weights = list(map(float ,weights.split(',')))
    impacts = list(map(str ,impacts.split(',')))

    # File not found handeled
    try:
        dataset = pd.read_csv(filename)
    except OSError:
        print("File not found")
        sys.exit() 

    data=dataset.iloc[ :,1:].values.astype(float)

    (r,c)=data.shape
    # Exception Handeled (Input file must contain three or more columns)
    if c < 3:
        print("Please enter three or more number of columns")

    s=sum(weights)

    # Exception handeled (Number of weights, number of impacts and number of columns (from 2nd to last columns) must be same.)
    if len(weights) != c:
        print("Enter the correct number of Weights")
        sys.exit()
    if len(impacts) != c:
        print("Enter the correct number of Impacts")
        sys.exit()

    # Exception handeled (Impacts must be either +ve or -ve)

    l = ['+','-']
    for i in impacts:
        if(i not in l):
            print(i)
            print("Invalid Impacts")
            sys.exit()


    for i in range(c):
        weights[i]/=s


    a=[0]*(c)


    for i in range(0,r):
        for j in range(0,c):
            a[j]=a[j]+(data[i][j]*data[i][j])

    for j in range(c):
        a[j]=np.sqrt(a[j])

    for i in range(r):
        for j in range(c):
            data[i][j]/=a[j]
            data[i][j]*=weights[j]

    ideal_positive=np.amax(data,axis=0) 
    ideal_negative=np.amin(data,axis=0) 
    for i in range(len(impacts)):
        if(impacts[i]=='-'):         
            temp=ideal_positive[i]
            ideal_positive[i]=ideal_negative[i]
            ideal_negative[i]=temp

    dist_pos=list()
    dist_neg=list()

    for i in range(r):
        s=0
        for j in range(c):
            s+=pow((data[i][j]-ideal_positive[j]), 2)

        dist_pos.append(float(pow(s,0.5)))


    for i in range(r):
        s=0
        for j in range(c):
            s+=pow((data[i][j]-ideal_negative[j]), 2)

        dist_neg.append(float(pow(s,0.5)))


    performance_score=dict()

    for i in range(r):
        performance_score[i+1]=dist_neg[i]/(dist_neg[i]+dist_pos[i])

    a=list(performance_score.values())
    b=sorted(list(performance_score.values()) , reverse=True)

    rank=dict()

    for i in range(len(a)):
        rank[(b.index(a[i]) + 1)] = a[i]
        b[b.index(a[i])] =-b[b.index(a[i])]


    row=list(i+1 for i in range(len(b)))
    a=list(rank.values())
    rr=list(rank.keys())


    out={'Row_NO':row,'Performance_score' : a , 'Rank':rr}

    output=pd.DataFrame(out)

    # Writing into the .csv file
    output.to_csv('result.csv',index=False)

    print(output)
