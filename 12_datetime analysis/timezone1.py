import pandas as pd
time_zone='America/New_York'
data=pd.read_csv('/Users/new algo trading/batch32/12_datetime analysis/data.csv')
data.drop([0,1],axis=0,inplace=True)


data.rename(columns={'Price':'Date'},inplace=True)
data['Date']=pd.to_datetime(data['Date'])
data['Date']=data['Date'].dt.tz_convert(time_zone)
data['Date']=data['Date'].dt.tz_localize(None)

print(data)
print(data.info())