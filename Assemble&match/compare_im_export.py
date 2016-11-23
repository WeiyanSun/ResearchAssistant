import pandas as pd
import numpy as np
import pdb
import csv

# define some variable
final_order=['CONSIGNEE','SHIPPER','Matching','Y/N','Keywords in address?','Matching keyword','FOREIGN PORT','US PORT', 'COUNTRY OF ORIGIN', 'CONSIGNEE ADDRESS', 'SHIPPER ADDRESS', 'Matching Country Name']

filter_col=['CONSIGNEE','SHIPPER','FOREIGN PORT','US PORT', 'COUNTRY OF ORIGIN', 'CONSIGNEE ADDRESS', 'SHIPPER ADDRESS']
add_col=['Matching','Y/N','Keywords in address?','Matching keyword','Matching Country Name']

kw_list=['INDUSTRIAL' ,'ZONE','PARK','EXPORT','ESTATE']

bad_word=["CO.,LTD.",
          "LLC",
          "CO.",
          "LTD.",
          'CORP.',
          'INC.',
          'PLANT.',
          'COMPANY',
          'GROUP',
          'LIMITED',
          'CORPORATION',
          'ADD:',
          'AND',
          'AS',
          'BEHALF',
          'OF','OF:'
          'DE',
          'FOR',
          'H',
          'GREAT',
          'INDUSTRIAL',
          'INDUSTRIES',
          'IND',
          'IND.',
          'INCORPORATED',
          'MFG',
          'MFG.',

         ]

poss_country=["M'SIA","CHINA","P.R.C.","VIETNAM","KOREA","TAIWAN","PHILIPPINES","PHILS","THAILAND","HONG KONG","HONGKONG","H.K","KOWLOON","JAPAN","INDIA","INDONESIA",",HK "," HK ","MALAYSIA","PH ILIPPINES","DUBAI",
"SINGAPORE","SWEDEN","NORWAY","FINLAND","GERMANY","NETHERLANDS","DENMARK","BELGIUM","FRANCE","SLOVAK","POLAND","HUNGARY","URUGUAY","TURKEY","AUSTRALIA","NEW ZEALAND","BRITISH VIR"," UK ","VIET NAM","SAUDI ARABIA",
"PERU","NICARAGUA","BRASIL","GUATEMALA","CHILE","EL SALVADOR","HONDURAS","COSTA RICAS","MAURITIUS","U.S.A","CAMBODIA","ITALY","SRI LANKA","MONGOLIA","PAKISTAN","COSTA RICA","COLOMBIA","PANAMA","VENEZUELA","BANGLADESH",
"SOUTH AFRICA","KLN","CANADA","UNITED STATES","SWITZERLAND","ECUADOR","NEPAL"]
# KLN: KOWLOON, VG: British Virgin Islands, LK: Sri Lanka, ID: indonesia, SG: Singapore
poss_abbr_country=["CN","VN","TW","PH","TH","HK","JP","UK","KR","MY","AU","NZ","VG","LK","BE","FR","IN","ID","SG"]

# create a dict for keyword match
def create_dict():
  kw_dict={}
  f=open("CN_prov.csv","r")
  for i in f:
    a_row=i.split(",")[0:-1]
    country=a_row[0]
    for kw in a_row[1::]:
      kw_dict[kw]=country
  f.close()
  return kw_dict


# define function

def match(la,row,i,bad_word):
    consignee=row["CONSIGNEE"]    
    shipper=row['SHIPPER'] 
    if type(shipper)==float:
      la.iloc[i,3]=0
      return la
    word_list=consignee.split(" ")
    dup_list=[]
    for word in word_list:
        if any(word in a for a in bad_word):
            #print(word)
            continue
        if word in shipper.split(" "):
            dup_list.append(word)
    if len(dup_list)==0:
        la.iloc[i,3]=0
    else:
        la.iloc[i,3]=1
        la.iloc[i,2]=" ".join(dup_list)
    return la

def match_zone(la,row,i):
  address=row["SHIPPER ADDRESS"]
  for word in kw_list:
    if word in address.upper():
      la.iloc[i,4]=1
      la.iloc[i,5]=word
      break
    else:
      la.iloc[i,4]=0
  return la

def match_country(la,row,i,kw_dict):
  address=row['SHIPPER ADDRESS']
  #pdb.set_trace()
  name=row['SHIPPER']
  find=False
  #if i==44:
  #  pdb.set_trace()
  # first filter: abbr country code, this should appear at the end of address. e.g THERE does not match TH
  last_str=address[-2::]
  for abbr in poss_abbr_country:
    if abbr in last_str:
      la.iloc[i,-1]=abbr
      find=True
      break
  # second filter, whole country name.
  if not find:
    for word in poss_country:
      if word in address:
        if word=='PERU':
          if address[-4::]=='PERU':
            la.iloc[i,-1]=word
            find=True
            break
        else:
          la.iloc[i,-1]=word
          find=True
          break
  # third filter, prov and city match in address or shipper name.
  if not find:
    for prov in list(kw_dict.keys()):
      if prov in address:
        la.iloc[i,-1]=kw_dict[prov]
        find=True
        break
      elif pd.notnull(name):
        if (prov in name):
          la.iloc[i,-1]=kw_dict[prov]
          find=True
          break
  return la



raw=pd.read_csv("los_angeles_1.csv")
la=raw[filter_col]
for col in add_col:
  la[col]=np.nan

la=la[final_order]

kw_dict=create_dict()

print("total ",len(la))
for i,row in la.iterrows():
  la=match(la,row,i,bad_word)
  la=match_zone(la,row,i)
  la=match_country(la,row,i,kw_dict)
  if i%5000==0:
  #if i==5000:
  #  break
    print (i)
  
la.to_csv("la_after_after.csv",index=False,quoting=csv.QUOTE_ALL)
    