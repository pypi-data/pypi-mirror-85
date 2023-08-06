import pandas as pd
import sys
import numpy as np
from os import path
from sys import exit
def main():
    if len(sys.argv)!=5:
        print("Incorrect number of parameters!!")
        exit(0)
    else:
        
           i=sys.argv[1]
           w=sys.argv[2]
           im=sys.argv[3]
           res=sys.argv[4]
           if not i.endswith('.csv'):
              print("Given file is not of the .csv format!!")
              exit(0)
           else:
               if not path.exists(i):
                  print("No such file exists!!")
                  exit(0)
               else:
                   f = pd.read_csv(i)
                   c = f.shape[-1]
                   if c<3:
                      print("File should have 3 or more columns!!")
                      exit(0)
                   p=0
                   for i in f.columns:
                       p=p+1
                       for j in f.index:
                           if p!=1:
                               val=isinstance(f[i][j],int)
                               val1=isinstance(f[i][j],float)
                               if not val and not val1:
                                   print(f'value is not numeric in {p} column')
                                   exit(0)
                   weight=w.split(',')
                   impact=im.split(',')
                   for i in range(0, len(weight)): 
                         weight[i] = int(weight[i])  
                         
                   if len(weight)!=len(impact) and len(weight)!=len(f.iloc[:,1:]):
                       print("no. of weight,impact and column form second to last must be same ")
                       exit(0)
                   else:
                       
                       for j in impact:
                          if j!='+' and j!='-':
                           print("impact must be + or -")
                           exit(0)
                       if w.count(",")*2+1!=len(w) and im.count(",")*2+1!=len(im):
                           print("weigth and impact must separate by commas")
                           exit(0)
                       else:
                           a=f.iloc[:,1:]
                           vp=[]
                           vn=[]
                           sp=[]
                           sn=[]
                           spn=[]
                           p=[]
                           for column in range(a.shape[1]):
                               sum=0
                               for row in range(a.shape[0]):
                                    sum=sum+a.iloc[row,column]**2
                               sum=sum**0.5
                               for i in range(a.shape[0]):
                                     a.iloc[i,column]=a.iloc[i,column]/sum
                               for j in range(a.shape[0]):
                                     a.iloc[j,column]=a.iloc[j,column]*weight[column]
        
                               if impact[column]=='+':
                                       vp.append(a.iloc[:,column].max())
                                       vn.append(a.iloc[:,column].min())
                               else:
                                      vp.append(a.iloc[:,column].min())
                                      vn.append(a.iloc[:,column].max())
    
                           for m in range(a.shape[0]):
                                 ans=0
                                 ans1=0
                                 for n in range(a.shape[1]):
                                       ans=ans+(a.iloc[m,n]-vp[n])**2
                                 ans=ans**0.5
                                 sp.append(ans)
        
                                 for o in range(a.shape[1]):
                                        ans1=ans1+(a.iloc[m,o]-vn[o])**2
                                 ans1=ans1**0.5
                                 sn.append(ans1)
                           for i in range(0,len(sp)):
                                spn.append(sp[i]+sn[i])
                           for i in range(0,len(spn)):
                                p.append(sn[i]/spn[i])
    
                           f.insert(5,"Topsis Score",p)
                           f.insert(6,"Rank",f["Topsis Score"].rank(ascending=False))
                           f.to_csv(res)
if __name__=="__main__":   
  main()  
                
                           
    
                       
            

       
                
