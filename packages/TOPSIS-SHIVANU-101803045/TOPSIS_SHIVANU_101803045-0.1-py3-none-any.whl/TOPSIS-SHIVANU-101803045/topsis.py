import pandas as pd
import math
import os
import sys

arguments = len(sys.argv)
flag = True


if arguments!=5:
    flag=False
    print("Enter right number of parameters")
else :
    inputfile=sys.argv[1]
    name,extension=os.path.splitext(sys.argv[1])
    if extension not in ['.csv']:
        flag=False
        print("File not Found ,Only csv file allowed")
    else :
        df=pd.read_csv(inputfile)
        row=df.shape[0]
        col=df.shape[1]
        df1 = df._get_numeric_data()
        col2 = df1.shape[1]
        if (col2 != (col - 1)):
            flag = False
            print("Only 1 column should be non numeric")

        if (df.columns.tolist()[1] != df1.columns.tolist()[0]):
            flag = False
            print("1st column should be non nummeric ,rest should be numeric")
        

        #print(col)
        if (col<3):
            flag=False
            print("Input file should have more than 3 column!")
        w=sys.argv[2]
        im=sys.argv[3]
        impact=[]
        for i in range(0,len(im)) :
            if(im[i]!=',') :
                impact.append(im[i])
        w=w+","
        wt=[]
        wti=[]
        st=0
        s=""
        for i in range(0,len(w)) :
            s=""
            if(w[i]==','):
                for j in range(st,i):
                    s=s+w[j]
                st=i+1
                wt.append(s)

        for i in range(0,len(wt)) :
            x=wt[i]
            t=float(x)
            wti.append(t)



        if((col-1)!=len(impact)):
            flag=False
            print("Please give correct number of impacts")

        if((col-1)!=len(wti)) :
            flag=False
            print("Please give correct number of weights!")



if flag==False:
    print("Try Again ,Wrong Input !")
else:
    norm_list=[]
    for i in range(1,col):
        sump=0
        for j in range(0,row) :
            x=df.iloc[j,i]
            sump=sump+(x*x)
        norm_list.append(math.sqrt(sump))	


    #print(norm_list) 

    c=0
    for i in range(1,col):
        for j in range(0,row):
            x=df.iloc[j,i]
            div=norm_list[c]
            x=x/div
            df.iloc[j,i]=x
        c=c+1 


      
    #print(df)

    c=0
    for i in range(1,col):
        for j in range(0,row):
            x=df.iloc[j,i]
            mul=wti[c]
            x=x*mul
            df.iloc[j,i]=x
        c=c+1 




    c=0
    Vp=[]
    Vn=[]
    for i in range(1,col):
        min=100
        max=0
        for j in range(0,row):
            x=df.iloc[j,i]
            if (x<min):
                min=x
            if(x>max):
                max=x
          
        if(impact[c]=='+'):
            Vp.append(max)
            Vn.append(min)
        else:
            Vp.append(min)
            Vn.append(max)
        c=c+1  

#Calculate S+ and S-
    Sp=[]
    Sn=[]

    for i in range(0,row):
        sum1=0
        sum2=0
        for j in range(1,col):
            x=df.iloc[i,j]
            diffp=x-Vp[j-1]
            sum1=sum1+(diffp*diffp)
            diffn=x-Vn[j-1]
            sum2=sum2+(diffn*diffn)
       
        Sp.append(math.sqrt(sum1))
        Sn.append(math.sqrt(sum2))

        
        

    Spn=[]
    for i in range(0,len(Sp)):
        x=Sp[i]+Sn[i]
        Spn.append(x)


    P=[]
    for i in range(0,len(Spn)) :
        x=Sn[i]/Spn[i]
        P.append(x)

    df['Performance']=0
 
    for i in range(0,col):
        df.iloc[i,col]=P[i]

    df['Rank']=0    

    c=0
    closed=[]
    while (c!=row):
        max=0
        p=0
        for i in range(0,col):
            if (df.iloc[i,col]>max)and(df.iloc[i,col] not in closed):
                max=df.iloc[i,col]
                p=i
        df.iloc[p,(col+1)]=c+1
        closed.append(df.iloc[p,col])
        c=c+1

    df.to_csv(sys.argv[4],index=False)                  
   