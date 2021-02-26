import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from function import getS,getUs,getMs,changeCol


ECU = pd.read_csv('data/ECU完整数据.csv', sep=',')
ECU['Timestamp']=ECU['Timestamp'].apply(lambda x:getMs(x))
ECU['Data']=ECU['Data'].apply(lambda x:int(x.replace(' ',''),16))
print(ECU)


dic = {'Fuel':'398','TP':'2C1','WSPD34':'0B2','WSPD12':'0B0','PRND':'3B4','SA':'25','ES':'2C4','BP':'224','AC':'380','OD':'611'}
ECUIDS=pd.DataFrame(ECU,columns=['Timestamp','ECUID','Data'])
ECUList = []
for i in dic:
    temp = locals()['ECU' + str(i)]=changeCol(ECUIDS,dic[i],i)
    ECUList.append(temp)

# ECUFuel=ECUIDS[ECUIDS.ECUID=='398'].rename(columns={'Data':'Fuel'}).drop(['ECUID'], axis=1).drop_duplicates(subset='Timestamp')
# ECUTP=ECUIDS[ECUIDS.ECUID=='2C1'].rename(columns={'Data':'TP'}).drop(['ECUID'], axis=1).drop_duplicates(subset='Timestamp')
# ECUWSPD34=ECUIDS[ECUIDS.ECUID=='0B2'].rename(columns={'Data':'WSPD34'}).drop(['ECUID'], axis=1).drop_duplicates(subset='Timestamp')
# ECUWSPD12=ECUIDS[ECUIDS.ECUID=='0B0'].rename(columns={'Data':'WSPD12'}).drop(['ECUID'], axis=1).drop_duplicates(subset='Timestamp')
# ECUPRND=ECUIDS[ECUIDS.ECUID=='3B4'].rename(columns={'Data':'PRND'}).drop(['ECUID'], axis=1).drop_duplicates(subset='Timestamp')
# ECUSA=ECUIDS[ECUIDS.ECUID=='25'].rename(columns={'Data':'SA'}).drop(['ECUID'], axis=1).drop_duplicates(subset='Timestamp')
# ECUES=ECUIDS[ECUIDS.ECUID=='2C4'].rename(columns={'Data':'ES'}).drop(['ECUID'], axis=1).drop_duplicates(subset='Timestamp')
# ECUBP=ECUIDS[ECUIDS.ECUID=='224'].rename(columns={'Data':'BP'}).drop(['ECUID'], axis=1).drop_duplicates(subset='Timestamp')
# ECUAC=ECUIDS[ECUIDS.ECUID=='380'].rename(columns={'Data':'AC'}).drop(['ECUID'], axis=1).drop_duplicates(subset='Timestamp')
# ECUOD=ECUIDS[ECUIDS.ECUID=='611'].rename(columns={'Data':'OD'}).drop(['ECUID'], axis=1).drop_duplicates(subset='Timestamp')

# ECUList = [ECUFuel,ECUTP,ECUWSPD12,ECUWSPD34,ECUPRND,
#            ECUSA,ECUES,ECUBP,ECUAC,ECUOD]


for i in ECUList:
  fig = plt.figure(figsize=(6,4)).add_subplot(111)
  time = str(i.columns[0])
  data = str(i.columns[1])
  fig.set_title(str(i.columns.values[1]),loc='left',fontsize='large',fontweight='bold',color='white')
  plt.ylabel('Data')
  plt.xlabel('Time(s)')
  fig.plot(i[time].values,i[data].values)
  plt.show()


for i in ECUList:
  max = int(i[i.columns[1]].max())
  min = int(i[i.columns[1]].min())
  #print(str(i.columns.values[1]) +" "+ str(imax)+" "+str(imin)+" "+str(imax-imin))
  i[i.columns.values[1]]=i[i.columns.values[1]].apply(lambda x:(int(x)-min)/(max-min))
for i in ECUList:
  print(i)


ECUnew = ECUList[0]
for i in ECUList[1:]:
  ECUnew = pd.merge(ECUnew,i,how='outer',on='Timestamp')
  #ECUnew = pd.merge(ECUnew,i,how='left',on='Timestamp')
ECUnew = ECUnew.sort_values(by='Timestamp')
print(ECUnew)



ECUnew.PRND=ECUnew.PRND.fillna(method='ffill')
ECUnew.AC=ECUnew.AC.fillna(method='ffill')
ECUnew.OD=ECUnew.OD.fillna(method='ffill')
#ECUnew.Fuel=ECUnew.Fuel.fillna(method='ffill')
#ECUnew.WSPD34=ECUnew.WSPD34.fillna(method='ffill')
print(ECUnew)


#ECUnew = ECUnew.dropna(axis=0,how='any')
ECUnew = ECUnew.dropna(axis=0,thresh=7)
ECUnew = ECUnew.interpolate()
ECUnew = ECUnew.dropna(axis=0,how='any')
ECUnew = ECUnew.drop(['Timestamp'],axis=1)


ECUnew.to_csv(path_or_buf=r'.\ECUnew.cvs',na_rep='NaN',header=False,index=False,index_label=None,mode='w')
print(ECUnew)


