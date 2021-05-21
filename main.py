#Import packages
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

#Set plot styles
plt.style.use('seaborn-colorblind')
plt.rcParams["font.family"] = "Times New Roman"

'''----------------------------------------------SET DATA PATHS ---------------------------------------------------- '''
data_path = "C:/Users/tjmor/OneDrive/Documents/Consulting/UAC_beacon/WBA_data/"

# load data
df_Bear_Trap = pd.read_csv(data_path + "BCC Bear Trap RAW.csv")
df_Bear_Trap.time = pd.to_datetime(df_Bear_Trap.time)
df_Butler = pd.read_csv("C:/Users/tjmor/OneDrive/Documents/Consulting/UAC_beacon/WBA_data/BCC Butler RAW.csv")
df_Butler.time = pd.to_datetime(df_Butler.time)
df_Cardiff = pd.read_csv("C:/Users/tjmor/OneDrive/Documents/Consulting/UAC_beacon/WBA_data/BCC Cardiff RAW.csv")
df_Cardiff.time = pd.to_datetime(df_Cardiff.time)

data_merge = pd.merge_asof(df_Bear_Trap, df_Butler, on='time')
data_merge = pd.merge_asof(data_merge, df_Cardiff, on='time')
data_merge = data_merge.rename(columns={'time':'DATE',' people_x':'NBearTrap',' people_y':'NButler','people':'NCardiff'})

# Set date column as index
data_merge = data_merge.set_index('DATE')


# Resample to daily sum of people
daily_avg = data_merge.resample('D').sum()
#pick the subset to plot
daily_avg_subTime = daily_avg.loc['2020-12-1 01:00:00':'2021-3-20 04:00:00']
#find weekends
#((pd.DatetimeIndex(daily_avg_subTime.index).dayofweek) // 5 == 1).astype(float)
'''---------------------------------------PLOT DAILY SUM FOR ALL THS-------------------------------------------------'''
#Butler
plt.figure(figsize=(10, 6))
plt.plot(daily_avg_subTime.index, daily_avg_subTime.NButler)
plt.title('WBA Butler')
plt.grid(b=bool, which='major', axis='both')
plt.ylabel('Number of people [N]')
plt.xticks(rotation=20) # Rotates X-Axis Ticks by 45-degrees
plt.autoscale(enable=True, axis='x', tight=True)
plt.legend(['Raw'], loc=2)
plt.show()
plt.savefig('books_read.png')
plt.close()
'''------------------------------------------------------------------------------------------------------------------'''
daily_stats = pd.DataFrame({"Sum": daily_avg.sum(axis=1)})
daily_stats.insert(1,"Avg",daily_avg.mean(axis=1),True)
daily_stats.insert(2,"Median",daily_avg.median(axis=1),True)
daily_stats.insert(3,"Std",daily_avg.std(axis=1),True)


daily_stats_subTime = daily_stats.loc['2020-12-1 01:00:00':'2021-3-20 04:00:00']
plt.figure()
#plt.scatter(daily_stats_subTime.index,daily_stats_subTime.Avg)
plt.errorbar(daily_stats_subTime.index, 'Avg', yerr='Std', data=daily_stats_subTime)
plt.show()

#fig1, ax1 = plt.subplots()
#ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
#ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
#plt.show()
