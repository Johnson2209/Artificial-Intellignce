# -*- coding: utf-8 -*-
"""Machine_Learning_Practical_3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ufsu4kDl0R0a6eRGHd7EgzrJd2-pmgVY

# PROPHET TIME SERIES -MAKING PREDICTION OF CRIME RATE IN CHICAGO USING FACEBOOK PROPHET

# Project Overview

* The Chicago dataset contains a summary of the reported crimes in the city of Chicago that occurred between 2001 and 2017
* Dataset has been obtained from the Chicago Police Department's CLEAR (Citizen Law Enforcement Analysis and Reporting) System
*
Data source :[link text](https://www.kaggle.com/currie32/crimes-in-chicago)

# Additional Tools to be Installed:

* Insatall fbprophet package as follows: pip install fbprophet

* Prophet is an Open Source Software released by Facebook's Core Data Science Team

* Prophet is a procedure for forecasting time-series data based on additive model where non-linear trends are fit with yearly, weekly, and daily seasonality, plus holiday effects.

* Prophet works best with time series that have strong seasonal effects and several seasons of historical data

* For more information, please checkout: [link text](https://research.fb.com/prophet-forecasting-at-scale/) or ,[link text](https://facebook.github.io/prophet/docs/quick_start.html#python-api)

# Section 1: Import Libraries and Data
"""

#! pip install fbprophet
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from fbprophet import Prophet

chicago_df_1 = pd.read_csv('Chicago_Crimes_2001_to_2004.csv', error_bad_lines =False)
chicago_df_2 = pd.read_csv('Chicago_Crimes_2005_to_2007.csv', error_bad_lines =False)
chicago_df_3 = pd.read_csv('Chicago_Crimes_2008_to_2011.csv', error_bad_lines =False)
chicago_df_4 = pd.read_csv('Chicago_Crimes_2012_to_2017.csv', error_bad_lines =False)

chicago_df_1.shape

chicago_df_2.shape

chicago_df_3.shape

chicago_df_4.shape

#concatenate the seperate dataframes into one
chicago_df = pd.concat([chicago_df_1,chicago_df_2, chicago_df_3, chicago_df_4], ignore_index=False, axis =0)
#chicago_df = pd.concat([chicago_df_2, chicago_df_3, chicago_df_4])

chicago_df.shape

"""# Section 2 : Exploring the Dataset"""

chicago_df.head()
#we are basically interested in the type of crime and the date it occured, so we can have an idea of the "seasonality of the crime"

plt.figure(figsize=(10,10))
sns.heatmap(chicago_df.isnull(), cbar = False, cmap= "YlGnBu")

chicago_df.drop(['Unnamed: 0', 'ID','Case Number', 'IUCR', 'X Coordinate', 'Y Coordinate', 'Updated On','Year','FBI Code', 'Beat','Ward', 'Community Area', 'Location','District', 'Longitude', 'Latitude'], inplace=True, axis =1)

chicago_df

# We will re-arrange our 'date-time format' by re-arranging our dataframe 'date"column
chicago_df.Date = pd.to_datetime(chicago_df.Date)

chicago_df.Date.tail(50)

#make the datetime column the index:
chicago_df.index = pd.DatetimeIndex(chicago_df.Date)

chicago_df

#Print out the different kind of crimes in our dataset
chicago_df['Primary Type'].value_counts()

#Print out the first 15 kind of crimes in our dataset
chicago_df['Primary Type'].value_counts().iloc[:15]

#Print out the index of the first 15 kind of crimes in our dataset
order_data = chicago_df['Primary Type'].value_counts().iloc[:15].index
order_data

plt.figure(figsize=(15,10))
sns.countplot(y = 'Primary Type', data=chicago_df,order=order_data)

plt.figure(figsize=(15,10))
sns.countplot(y = 'Location Description', data=chicago_df,order= chicago_df['Location Description'].value_counts().iloc[:15].index)

#crimes per specific years
chicago_df.resample('Y').size()

#plot crimes per specific years
plt.plot(chicago_df.resample('Y').size())
plt.title('Crime counts per year')
plt.xlabel('Year')
plt.ylabel('Number of Crime per year')

#plot crimes per specific months
plt.plot(chicago_df.resample('M').size())
plt.title('Crime counts per Month')
plt.xlabel('Month')
plt.ylabel('Number of Crime per Month')

#plot crimes per Quarter
plt.plot(chicago_df.resample('Q').size())
plt.title('Crime counts per Quarter')
plt.xlabel('Quarter')
plt.ylabel('Number of Crime per Month')

"""# Section 3: Preparing the Data"""

chicago_prophet =chicago_df.resample('M').size().reset_index()

#this gives the number of crimes per month
chicago_prophet

chicago_prophet.columns = ['Date','Crime Count']

chicago_prophet

# Very important step: Recast the columns in 'ds' and 'y' format
chicago_prophet_final =chicago_prophet.rename(columns={'Date':'ds','Crime Count':'y'})

chicago_prophet_final

"""# Section 3: Make Prediction"""

m =Prophet()
m.fit(chicago_prophet_final)

# We want to predict what happens over the next three years(2017-2021)
future = m.make_future_dataframe(periods =1095)
forecast =m.predict(future)

forecast

figure = m.plot(forecast, xlabel= 'Date', ylabel= 'Crime Rate')

figure = m.plot_components(forecast)

"""# Conclusion:
* Our prediction a decreasing trend in crime rate over the next three years(2017-2020)
* The seasonality: Crime rate is highest in Mar-Dec, and lowest between Sep-Dec
"""

