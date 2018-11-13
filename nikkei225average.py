import pandas as pd
import numpy as np
from fbprophet import Prophet
import matplotlib.pyplot as plt
import os

df = pd.read_csv('^N225.csv')

df2 = df.loc[:,['Date','Close']]
df2 = df2.rename(columns={'Date':'ds','Close':'y'})

m = Prophet()
m.daily_seasonality = True
m.fit(df2)

future = m.make_future_dataframe(periods=3650)
future.tail()

forecast = m.predict(future)

fig = m.plot(forecast)
m.plot_components(forecast)
plt.show()
