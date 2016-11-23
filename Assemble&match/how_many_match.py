import pandas as pd
import os

path="C:\\Users\\victor.sun\\Downloads\\los_angeles_Victor"


count_df=pd.DataFrame(columns=['csv_name','no_match_count','total_len','match_proportion'])
i=0
for file in os.listdir(path):
  row=[]
  temp=pd.read_csv(path+"\\"+file,encoding = "ISO-8859-1")
  row.append(file)
  miss=temp['Matching Country Name'].isnull()
  row.append(miss.sum())
  row.append(len(miss))
  row.append(1-miss.sum()/len(miss))
  count_df.loc[i]=row
  i+=1

count_df.to_csv('count_la.csv',index=False)


