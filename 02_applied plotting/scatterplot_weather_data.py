import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.ticker as ticker
import numpy as np
#%matplotlib notebook

wt = pd.read_csv('data/weather_data_ffm.csv')
    
# Convert date to datetime
wt['Date'] = pd.to_datetime(wt['Date'], format='%Y-%m-%d')
    
# Convert temperature to degrees Celsius
wt['Data_Value'] *= .1
    
# Get year of each measurement
wt['Year'] = wt['Date'].dt.year
    
# Get month and day of each measurement
wt['Month_Day'] = wt['Date'].dt.strftime('%m-%d')
    
# Remove February 29
wt = wt[wt['Month_Day']!='02-29']

# Find record highs and lows (2005-2014)
wt_highs = wt[(wt.Year>=2005) & (wt.Year<2015) & (wt.Element=='TMAX')].groupby(['Month_Day'])['Data_Value'].max()
wt_lows = wt[(wt.Year>=2005) & (wt.Year<2015) & (wt.Element=='TMIN')].groupby(['Month_Day'])['Data_Value'].min()

# Create datetime index
date_idx = np.arange('2015-01-01', '2016-01-01', dtype='datetime64[D]')

# Plot highs and lows
plt.figure(figsize=(10,7))
plt.plot(date_idx, wt_highs, color='coral', linewidth=1)
plt.plot(date_idx, wt_lows, color='skyblue', linewidth=1)
plt.xlabel('Date', fontsize=12)
plt.ylabel('° Celsius', fontsize=12)

# Set axis
ax = plt.gca()
ax.axis(['2015-01-01', '2015-12-31', -20, 47])

# Set months as axis ticks (centered)
ax.xaxis.set_major_locator(dates.MonthLocator())
ax.xaxis.set_minor_locator(dates.MonthLocator(bymonthday=15))
ax.xaxis.set_major_formatter(ticker.NullFormatter())
ax.xaxis.set_minor_formatter(dates.DateFormatter('%b'))
for tick in ax.xaxis.get_minor_ticks():
    tick.tick1line.set_markersize(0)
    tick.tick2line.set_markersize(0)
    tick.label1.set_horizontalalignment('center')
    

# Plot scatter points
wt = wt.merge(wt_highs.reset_index(drop=False).rename(columns={'Data_Value':'Max_temp'}), 
              on='Month_Day',
              how='left')
wt = wt.merge(wt_lows.reset_index(drop=False).rename(columns={'Data_Value':'Min_temp'}), 
              on='Month_Day',
              how='left')

breaking_high = wt[(wt.Year==2015)&(wt.Data_Value>wt.Max_temp)]
breaking_low = wt[(wt.Year==2015)&(wt.Data_Value<wt.Min_temp)]

plt.scatter(breaking_high.Date.values, breaking_high.Data_Value.values, color='red');
plt.scatter(breaking_low.Date.values, breaking_low.Data_Value.values, color='Blue');

# Set legend and title
plt.legend(['Record high 2005-2014',
           'Record low 2005-2014',
           'Day in 2015 that broke the record high',
           'Day in 2015 that broke the record low'],
          loc = 'lower center', frameon=False)

plt.title('Weather Patterns Frankfurt a.M, Germany (2005-2015)')

# Fill area between min and max
ax.fill_between(date_idx, wt_highs, wt_lows, color='lightgray', alpha=0.25)