import pandas as pd
from matplotlib import pyplot as plt

# read data
dhw_usage = pd.read_csv('Data/DHW_Usage.csv', header=0, index_col=0, parse_dates=[0])
temperature_data = pd.read_csv('Data/T_weather_environment temperature_1809_1908.csv', header=0,
                               index_col=0, parse_dates=[0])
ventilation_data = pd.read_csv('Data/OE003.csv', header=0,
                               index_col=0, parse_dates=[0])
# get the frequency of the original data, prepare for rolling method
dhw_timeline_frequency_s = (dhw_usage.index[1] - dhw_usage.index[0]).seconds
t_timeline_frequency_s = (temperature_data.index[1] - temperature_data.index[0]).seconds
v_timeline_frequency_s = (ventilation_data.index[1] - ventilation_data.index[0]).seconds

# some key settings.
hourly_averaged = 3  # the data are averaged by 3 hours
days_analysed = 10  # data used

dhw_usage_hourly_averaged = dhw_usage.rolling(
    window=int(hourly_averaged * 3600 / dhw_timeline_frequency_s),
    center=True).mean()
temperature_hourly_averaged = temperature_data.rolling(
    window=int(hourly_averaged * 3600 / t_timeline_frequency_s),
    center=True).mean()
ventilation_hourly_averaged = ventilation_data.rolling(
    window=int(hourly_averaged * 3600 / v_timeline_frequency_s),
    center=True).mean()

# reindex the data to a same timeline
reindex_frequency_s = hourly_averaged * 3600
reindex_timeline = pd.date_range(pd.Timestamp('20180831 23:00:00'), pd.Timestamp('20190831 23:00:00'),
                                 freq=pd.Timedelta('{}s'.format(reindex_frequency_s)))
DHW_usage_reindex = dhw_usage_hourly_averaged.reindex(reindex_timeline)
temperature_data_reindex = temperature_hourly_averaged.reindex(reindex_timeline)
ventilation_data_reindex = ventilation_hourly_averaged.reindex(reindex_timeline)

# the correlation between DHW usage and its records
corr_coefs = []
for i in range(int(days_analysed * 24 / hourly_averaged)):
    temp = DHW_usage_reindex.shift(i)
    temp = pd.concat([temp, DHW_usage_reindex], axis=1)
    temp_corr = temp.corr().iloc[1, 0]
    corr_coefs.append(temp_corr)
plt.plot(corr_coefs, '.-')
plt.xlabel('i-th step ahead DHW usage records')
plt.ylabel('Correlation Coefficient')
plt.title('Hourly Averaged: {}'.format(hourly_averaged))
plt.savefig('Pics/DHW Usage Records.png', dpi=300)
plt.show()

# the correlation between DHW usage and temperature records
t_corr_coefs = []
for i in range(int(days_analysed * 24 / hourly_averaged)):
    temp = temperature_data_reindex.shift(i)
    temp = pd.concat([temp, DHW_usage_reindex], axis=1)
    temp_corr = temp.corr().iloc[1, 0]
    t_corr_coefs.append(temp_corr)
plt.plot(t_corr_coefs, '.-')
plt.xlabel('i-th step ahead temperature records')
plt.ylabel('Correlation Coefficient')
plt.title('Hourly Averaged: {}'.format(hourly_averaged))
plt.savefig('Pics/Temperature Records.png', dpi=300)
plt.show()

# the correlation between DHW usage and ventilation records
v_corr_coefs = []
for i in range(int(days_analysed * 24 / hourly_averaged)):
    temp = ventilation_data_reindex.shift(i)
    temp = pd.concat([temp, DHW_usage_reindex], axis=1)
    temp_corr = temp.corr().iloc[1, 0]
    v_corr_coefs.append(temp_corr)
plt.plot(v_corr_coefs, '.-')
plt.xlabel('i-th step ahead ventilation records')
plt.ylabel('Correlation Coefficient')
plt.title('Hourly Averaged: {}'.format(hourly_averaged))
plt.savefig('Pics/Ventilation Records.png', dpi=300)
plt.show()
