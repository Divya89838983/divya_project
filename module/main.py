import numpy as np
import pandas as pd

#ML model training
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import kpss
from statsmodels.tsa.arima.model import ARIMA
import itertools


#Data fetching
complete_data = pd.read_excel('data.csv', header=[0,1])
complete_data.head()

all_stations = complete_data.iloc[1931:]
all_stations.head()

all_stations['Date'] = pd.to_datetime(all_stations['From Date']['From Date'], format='%d-%b-%Y - %H:%M')
all_stations.drop(columns=['From Date', 'To Date'], inplace=True)
all_stations.head()

