#!/usr/bin/env python
# coding: utf-8

# In[1]:


#IMPORT THE REQUIRED LIBRARIES
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


# INCREASE THE ROW COUNT
pd.set_option("display.max_rows",1000)


# In[34]:


#IMPORT THE TIME SERIES CSV FILES from  https://data.humdata.org/dataset/novel-coronavirus-2019-ncov-cases.
#Novel Corona Virus (COVID-19) epidemiological data since 22 January 2020. The data is compiled by the Johns Hopkins University Center for Systems Science and Engineering (JHU CCSE) from various sources including the World Health Organization (WHO), DXY.cn. Pneumonia. 2020, BNO News, National Health Commission of the People’s Republic of China (NHC), China CDC (CCDC), Hong Kong Department of Health, Macau Government, Taiwan CDC, US CDC, Government of Canada, Australia Government Department of Health, European Centre for Disease Prevention and Control (ECDC), Ministry of Health Singapore (MOH). JSU CCSE maintains the data on the 2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository on github.
#https://github.com/CSSEGISandData/COVID-19

import datetime
start = datetime.datetime.now()
url_confirmed = "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv"
url_death = "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_deaths_global.csv&filename=time_series_covid19_deaths_global.csv"
url_recovered = "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_recovered_global.csv&filename=time_series_covid19_recovered_global.csv"
dataframe_confirmed = pd.read_csv(url_confirmed,index_col=None,parse_dates=[0])
dataframe_death = pd.read_csv(url_death,index_col=None,parse_dates=[0])
dataframe_recovered = pd.read_csv(url_recovered,index_col=None,parse_dates=[0])
finish = datetime.datetime.now()
print (finish-start)


# In[4]:


#CHECK FOR THE RECENT AVAILABLE DATE IN THE DATASOURCE

from datetime import datetime, timedelta

a = datetime.now()-timedelta(days=0)
b = datetime.now()-timedelta(days=1)
c=  datetime.now()-timedelta(days=2)
d=  datetime.now()-timedelta(days=3)

a=str(a.strftime('X%m/X%d/%y').replace('X0','X').replace('X',''))
b=str(b.strftime('X%m/X%d/%y').replace('X0','X').replace('X',''))
c=str(c.strftime('X%m/X%d/%y').replace('X0','X').replace('X',''))
d=str(d.strftime('X%m/X%d/%y').replace('X0','X').replace('X','')) 

w = a in dataframe_confirmed
x = b in dataframe_confirmed
y = c in dataframe_confirmed
z = d in dataframe_confirmed

if  w ==True:
    current_date = a
    previous_date = b
elif  x==True:
    current_date = b
    previous_date = c
else :
    current_date = c
    previous_date = d

print(" The latest available date in the CSV file is---  " +  current_date )


# In[5]:


# Clean up all the NaN with the value and replace it with the value '0'
dataframe_confirmed.fillna(0,inplace = True)
dataframe_death.fillna(0,inplace = True)
dataframe_recovered.fillna(0,inplace = True)


# In[6]:


# KNOW MORE ABOUT THE DATA IN THE DATAFRAME

dataframe_confirmed.info()
#dataframe_death.info()
#dataframe_recovered.info()


# In[7]:


# See how many times each country repeats

dataframe_confirmed['Country/Region'].value_counts()
#dataframe_death['Country/Region'].value_counts()
#dataframe_recovered['Country/Region'].value_counts()


# In[8]:


# TOTAL NUMBER OF NUNIQUE ENTRIES IN THE DATA SOURCE
dataframe_confirmed['Country/Region'].nunique()
#dataframe_death['Country/Region'].nunique()
#dataframe_recovered['Country/Region'].nunique()


# In[9]:


#DATASET CONCATENATION 
recovered_groupby=dataframe_recovered.groupby('Country/Region').sum()
confirmed_groupby=dataframe_confirmed.groupby('Country/Region').sum()
death_groupby=dataframe_death.groupby('Country/Region').sum()
combined_data=pd.concat([confirmed_groupby,recovered_groupby,death_groupby],keys=["Confirmed","Recovered","Deaths"])
combined_data


# In[10]:


#GLOBAL SUMMARY
World_confirmed=combined_data.loc[("Confirmed"),current_date].sum()
World_recovered=combined_data.loc[("Recovered"),current_date].sum()
World_deceased=combined_data.loc[("Deaths"),current_date].sum()
World_recovered_percent=(combined_data.loc[("Recovered"),current_date].sum()/combined_data.loc[("Confirmed"),current_date].sum())*100
World_deceased_percent=(combined_data.loc[("Deaths"),current_date].sum()/combined_data.loc[("Confirmed"),current_date].sum())*100

print("Total Confirmed---  " + str(World_confirmed)+"\n" 
      "Total Recovered---   " + str(World_recovered)+" ---i.e. " + str(round(World_recovered_percent)) + "% of Total Confirmed"+"\n"
      "Total Deaths------   " + str(World_deceased)+" ---i.e. " + str(round(World_deceased_percent)) + "% of Total Confirmed"+"\n") 


# In[11]:


#FIND THE ACTIVE CASES = Confirmed - Recovered - Deaths = Active Cases
confirmed_groupby=dataframe_confirmed.groupby('Country/Region')
a=confirmed_groupby[[previous_date,current_date]].sum()
recovered_groupby=dataframe_recovered.groupby('Country/Region').sum()
confirmed_groupby=dataframe_confirmed.groupby('Country/Region').sum()
death_groupby=dataframe_death.groupby('Country/Region').sum()
combined_data=pd.concat([confirmed_groupby,recovered_groupby,death_groupby],keys=["Confirmed","Recovered","Deaths"])

a['Confirmed']=combined_data.loc[("Confirmed"),current_date]
a['Recovered']=combined_data.loc[("Recovered"),current_date]
a['Deaths'] =combined_data.loc[("Deaths"),current_date]
a['Active'] = (combined_data.loc[("Confirmed"),current_date])-(combined_data.loc[("Recovered"),current_date])-(combined_data.loc[("Deaths"),current_date])
a[['Confirmed','Recovered','Deaths','Active']].sort_values('Active', ascending = False)


# In[12]:


# RANK COUNTRY CASES RANKWISE
confirmed_groupby=dataframe_confirmed.groupby('Country/Region')
b=confirmed_groupby[[previous_date,current_date]].sum()
b['Confirmed Case Ranking']= b[current_date].rank(ascending=False).astype("int")
b["% increase in cases from Previous Day"] = (round(((b[current_date]-b[previous_date])/b[previous_date])*100))
b.sort_values(by = current_date,ascending = False)


# In[13]:


# CONFIRMED CASES IN EACH COUNTRY FOR CURRENT AND THE PREVIOUS DAY
confirmed_groupby=dataframe_confirmed.groupby('Country/Region')
e=confirmed_groupby[[previous_date,current_date]].sum()
e["Case increase from Previous Day"] = (e[current_date]-e[previous_date])
e["% increase in cases per day"] = ((e[current_date]-e[previous_date])/e[previous_date])*100
e.sort_values(by = "Case increase from Previous Day",ascending = False)


# In[14]:


# WHICH COUNTRY HAS 15000 cases and more than 10% increase in case from the previous day
confirmed_groupby=dataframe_confirmed.groupby('Country/Region').sum()
confirmed_groupby["% increase in cases per day"] = ((confirmed_groupby[current_date]-confirmed_groupby[previous_date])/confirmed_groupby[previous_date])*100

mask1 = confirmed_groupby[current_date]>15000
mask2 = confirmed_groupby["% increase in cases per day"] > 3.5

confirmed_groupby[[previous_date,current_date,"% increase in cases per day"]][mask1 & mask2].sort_values(by ='% increase in cases per day',ascending = False)


# In[15]:


# No increase has been reported from previous day
confirmed_groupby=dataframe_confirmed.groupby('Country/Region').sum()
confirmed_groupby["% increase in cases per day"] = ((confirmed_groupby[current_date]-confirmed_groupby[previous_date])/confirmed_groupby[previous_date])*100
mask2 = confirmed_groupby["% increase in cases per day"].isin(['0'])
confirmed_groupby[[previous_date,current_date,"% increase in cases per day"]][mask2].sort_values(by ='% increase in cases per day',ascending = False)


# In[16]:


# SORT BY PERCENTAGE INCREASE
a["% increase in cases per day"] = ((a[current_date]-a[previous_date])/a[previous_date])*100
a.sort_values(by = "% increase in cases per day",ascending = False)


# In[17]:


#Cases above 50000

#mask = confirmed_groupby[current_date]>1000
#confirmed_groupby[mask].sort_values(by = current_date,ascending = False)


# In[18]:


#Which country has the maximum cases
confirmed_groupby=dataframe_confirmed.groupby('Country/Region').sum()
confirmed_groupby[current_date].idxmax()


# In[19]:


#Which country has the minimum cases
confirmed_groupby=dataframe_confirmed.groupby('Country/Region').sum()
confirmed_groupby[current_date].idxmin()


# In[20]:


#FIND TOP 10 COUNTRIES WITH HIGHEST RECOVERY
recovered_groupby=dataframe_recovered.groupby('Country/Region').sum()
recovered_groupby[current_date].nlargest(10)


# In[21]:


#FIND TOP 10 COUNTRIES WITH HIGHEST RECOVERY PERCENTAGES
a['Recovery %'] = (((combined_data.loc[("Recovered"),current_date])/(combined_data.loc[("Confirmed"),current_date]))*100)
a[['Confirmed','Recovered','Recovery %']].sort_values(['Recovery %','Recovered'], ascending = False)


# In[22]:


#FIND TOP 10 COUNTRIES WITH HIGHEST DEATH RATES
death_groupby=dataframe_death.groupby('Country/Region').sum()
death_groupby[current_date].nlargest(10)


# In[23]:


#Highest Cases - Confirmed Recovered , Active & Death reported
confirmed_groupby=dataframe_confirmed.groupby('Country/Region')
b=confirmed_groupby[[previous_date,current_date]].sum()
b['Confirmed']=combined_data.loc[("Confirmed"),current_date]
b['Recovered']=combined_data.loc[("Recovered"),current_date]
b['Death'] =combined_data.loc[("Deaths"),current_date]
b['Active'] = (combined_data.loc[("Confirmed"),current_date])-(combined_data.loc[("Recovered"),current_date])-(combined_data.loc[("Deaths"),current_date])
b['Recovery %']=(round(combined_data.loc[("Recovered"),current_date] / combined_data.loc[("Confirmed"),current_date] *100))
b['Death %']=(round(combined_data.loc[("Deaths"),current_date] / combined_data.loc[("Confirmed"),current_date] *100))
l=(combined_data.loc[("Confirmed"),current_date])-(combined_data.loc[("Recovered"),current_date])-(combined_data.loc[("Deaths"),current_date])
b['Active %']=(round((l / combined_data.loc[("Confirmed"),current_date]) *100))

b[['Confirmed','Recovered','Active','Death','Recovery %','Active %','Death %']].sort_values(['Recovered','Recovery %'], ascending = False)
#b[['Confirmed','Recovered','Active','Death','Recovery %','Active %','Death %']].sort_values(['Active','Active %'], ascending = False)
#b[['Confirmed','Recovered','Active','Death','Recovery %','Active %','Death %']].sort_values(['Death','Death %'], ascending = False)


# In[24]:


#% Comparision

mask1 = b["Confirmed"]>10000
mask2 = b['Death %'] > 7
b[['Confirmed','Recovered','Active','Death','Recovery %','Active %','Death %']][mask1 & mask2].sort_values('Death %', ascending = False)


# In[25]:


#TOTAL OF EACH COUNTRY 
#MS Zaandam
#Diamond Princess


Country = "United Kingdom"

confirmed_groupby=dataframe_confirmed.groupby('Country/Region').sum()
confirmed_cases_in=str(confirmed_groupby.at[Country,current_date])
recovered_cases_in=str(recovered_groupby.at[Country,current_date])
deaths_reported_in= str(death_groupby.at[Country,current_date])
active_cases=str((confirmed_groupby.at[Country,current_date])-(recovered_groupby.at[Country,current_date])-(death_groupby.at[Country,current_date]))
print ("Country"+"\t"+"\t"+ Country +"\n"
       "Data "+"\t"+"\t"+current_date+"\n"
     "Confirmed Cases" +"\t"+ confirmed_cases_in+ "\n"+ 
      "Recovered Cases" +"\t"+ recovered_cases_in +"\n"+
      "Deaths Reported"+"\t"+ deaths_reported_in+ "\n"+
      "Active Cases"+"\t"+ active_cases) 


# In[26]:


import seaborn as sns
import matplotlib.pyplot as plt


confirmed_groupby=dataframe_confirmed.groupby('Country/Region')
h=confirmed_groupby[[previous_date,current_date]].sum()
h['Confirmed']=combined_data.loc[("Confirmed"),current_date]
h['Recovered']=combined_data.loc[("Recovered"),current_date]
h['Deaths'] =combined_data.loc[("Deaths"),current_date]
#mask1 = h["Confirmed"]>10000
#mask2 = h['Death %'] > 7
h=h[['Confirmed','Recovered','Deaths']].sort_values('Confirmed', ascending = False).head(15)
h.reset_index(inplace=True)


sns.set(style="whitegrid",font_scale=3)


# Initialize the matplotlib figure
f, ax = plt.subplots(figsize=(25, 25))

# Load the example car crash dataset
#crashes = sns.load_dataset("car_crashes").sort_values("total", ascending=False)

# Plot the total crashes
sns.set_color_codes("muted")
sns.barplot(x="Confirmed", y="Country/Region", data=h,
            label="Total", color="b")

# Plot the crashes where alcohol was involved
sns.set_color_codes("pastel")
sns.barplot(x="Recovered", y="Country/Region", data=h,
            label="Recovered", color="b")

sns.set_color_codes("dark")
sns.barplot(x="Deaths", y="Country/Region", data=h,
            label="Deaths", color="b")

# Add a legend and informative axis label
ax.legend(ncol=2, loc="lower right", frameon=True)
ax.set(xlim=(0, 900000), ylabel="",
       xlabel="Pandemic Cases")
#ax.set_xlabel("X Label",fontsize=30)

sns.despine(left=True, bottom=True)


# In[27]:


#HEATMAP, DEATHS TO CONFIRMED CASES

import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

# Load the example flights dataset and convert to long-form

flights = h.pivot("Country/Region", 'Confirmed','Deaths')

# Draw a heatmap with the numeric values in each cell
f, ax = plt.subplots(figsize=(15, 10))
sns.heatmap(flights, annot=True, fmt="g", linewidths=.5, ax=ax)


# In[28]:


# CONFIRMED CASE GRAPH
import warnings
warnings.simplefilter(action='ignore')

confirmed_groupby=dataframe_confirmed.groupby('Country/Region').sum()
confirmed=dataframe_confirmed.groupby('Country/Region').sum().sort_values(by = current_date,ascending = False)
confirmed.reset_index(inplace=True)
del confirmed_groupby['Lat']
del confirmed_groupby['Long']

  
a=confirmed['Country/Region']
a
columns = list(a) 
f, axes = plt.subplots(5,5,figsize=(25,25))

x = [0,0,0,0,0,1,1,1,1,1,2,2,2,2,2,3,3,3,3,3,4,4,4,4,4,5,5,5,5,5]
y = [0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4]

for i,c,v in zip(columns,x,y):
     confirmed_groupby.loc[i].plot(kind='line',xlim=(0,100),ylim=(0,900000),color='red',logy=True , ax=axes[c,v],title=i.upper())
            
f.tight_layout(pad=3.0)     
    
  


# In[ ]:





# In[29]:


f, axes = plt.subplots(3,4,figsize=(20,15))
k1 = confirmed_groupby.loc['US'].plot(kind='line',xlim=(0,100),ylim=(0,900000),color='red',logy=True , ax=axes[0,0],title='US')
k2 = confirmed_groupby.loc['Spain'].plot(kind='line',xlim=(0,100),ylim=(0,900000),color='red',logy=True , ax=axes[0,1],title='Spain')
k3 = confirmed_groupby.loc['India'].plot(kind='line',xlim=(0,100),ylim=(0,900000),color='red',logy=True , ax=axes[1,0],title='India')
confirmed_groupby.loc['China'].plot(kind='line',xlim=(0,100),ylim=(0,900000),color='red',logy=True , ax=axes[1,1],title='China')


# In[30]:


confirmed_groupby=dataframe_confirmed.groupby('Country/Region').sum()
del confirmed_groupby['Lat']
del confirmed_groupby['Long']
f, axes = plt.subplots(3,4,figsize=(20,15))
k1 = confirmed_groupby.loc['US'].plot(kind='line',xlim=(0,100),ylim=(0,900000),color='red',logy=True , ax=axes[0,0],title='US')
k2 = confirmed_groupby.loc['Spain'].plot(kind='line',xlim=(0,100),ylim=(0,900000),color='red',logy=True , ax=axes[0,1],title='Spain')
k3 = confirmed_groupby.loc['India'].plot(kind='line',xlim=(0,100),ylim=(0,900000),color='red',logy=True , ax=axes[1,0],title='India')
confirmed_groupby.loc['China'].plot(kind='line',xlim=(0,100),ylim=(0,900000),color='red',logy=True , ax=axes[1,1],title='China')


# In[31]:


confirmed_groupby=dataframe_confirmed.groupby('Country/Region').sum()
del confirmed_groupby['Lat']
del confirmed_groupby['Long']

#plt.rcParams['figure.figsize']=5,3

#confirmed_groupby.loc['US'].plot(ls='--',marker='s',ms=1)
#plt.plot(confirmed_groupby.loc['Spain'], c='Red',ls='--',logx=True)
#plt.xticks( np.arange(0, 100, step=10),rotation= 'vertical')
#ax=plt.gca()
#ax.set_xlim([0,10])


confirmed_groupby.loc['India'].plot(kind='line',xlim=(0,100),ylim=(0,900000),color='red',logy=True)
#plt.xlabel("Date")
#plt.ylabel("No of Cases")
#plt.title("Spain")
#plt.show()

plt.tight_layout()
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




