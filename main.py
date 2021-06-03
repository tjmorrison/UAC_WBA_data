"""
WBA PEOPLE COUNTING PROCESSING CODE
AUTHOR: Travis Morrison
DATE: 5-21-2021
SUMARRY: This code process the people data for the 2020-2021 season by plotting the raw time series, adjusting for
calibrations, and doing some statistics on the entire data set
TO DOS: Identify weekends and add shading to figures
"""

'''---------------------------------------------IMPORT PACKAGES -----------------------------------------------------'''
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

'''----------------------------------------------PLOT SETTINGS ------------------------------------------------------'''
plt.style.use('seaborn-colorblind') # Color Scheme for plots
plt.rcParams["font.family"] = "Times New Roman" # Font style
'''----------------------------------------------SET DATA PATHS ---------------------------------------------------- '''
data_path = "C:/Users/tjmor/OneDrive/Documents/Consulting/UAC_beacon/WBA_data/"
saveTSFig_path = "C:/Users/tjmor/OneDrive/Documents/Consulting/UAC_beacon/WBA_Figures/Raw_Timeseries/"
'''--------------------------------------------LOAD/PREPARE DATA ----------------------------------------------------'''
files = ['BCC Bear Trap RAW.csv', 'BCC Butler RAW.csv', 'BCC Cardiff RAW.csv', 'BCC Days Fork RAW.csv',
         'BCC Mill B South RAW.csv', 'BCC Mill D RAW.csv', 'BCC Mineral Fork RAW.csv', 'BCC Silver Fork RAW.csv',
         'BCC Willow Heights RAW.csv', 'LCC Our Lady East RAW.csv', 'LCC Our Lady RAW.csv', 'LCC Summer Road RAW.csv',
         'LCC White Pine RAW.csv', 'MCC Porter RAW.csv', 'MCC Road RAW.csv']

df = {} # this creates a blank collection of data frames
df_merge = pd.DataFrame(columns=['time']) # creates the blank dataframe with column called time
for ii in files:
    df[ii] = pd.read_csv(data_path + ii)
    df[ii].time = pd.to_datetime(df[ii].time) # Convert the time column to time format
    df_merge = df_merge.merge(df[ii], on='time', how='outer') # Merge the time series data

# Change the name of the columns to something more descriptive
df_merge.columns = ['DATE', 'NBearTrap', 'NButler', 'NCardiff', 'NDays', 'NMillB', 'NMillD', 'NMineral', 'NSilver',
                    'NWillow', 'NOurLadyE', 'NOurLady', 'NSumRd', 'NWhitePine', 'NPorter', 'NMCRd']

# Set time column as index
data_merge = df_merge.set_index('DATE')

# Resample to daily sum of people
daily_avg = data_merge.resample('D').sum()

# pick the time subset to plot
daily_avg_subTime = daily_avg.loc['2020-12-1 01:00:00':'2021-5-20 04:00:00']

#find weekends~ still need to work on this
#((pd.DatetimeIndex(daily_avg_subTime.index).dayofweek) // 5 == 1).astype(float)
'''---------------------------------------PLOT DAILY SUM FOR ALL THS-------------------------------------------------'''
titles = ['BearTrap', 'Butler', 'Cardiff', 'Days', 'Mill B', 'Mill D', 'Mineral', 'Silver Fork',
          'Willow Heights', 'Our Lady of the Snow E', 'Our Lady of the Snow', 'Grizzly Road', 'White Pine',
          'Porter Fork', 'Mill Creek Road']
# plots all individual figures
cnt = 0
for column in daily_avg_subTime:
    plt.figure(figsize=(10, 6))
    plt.plot(daily_avg_subTime.index, daily_avg_subTime[column])
    plt.title('WBA ' + titles[cnt] + ' Daily Total')
    plt.minorticks_on()
    plt.grid(b=bool, which='major', axis='both')
    plt.ylabel('Number of people [N]')
    plt.xticks(rotation=20)
    plt.autoscale(enable=True, axis='x', tight=True)
    plt.legend(['Raw'], loc=2) # legend in upper left side
    plt.show()
    #plt.savefig(saveTSFig_path+titles[cnt]+'.png')
    plt.close()
    cnt = cnt+1

# Plot all times series on one figure
cnt = 0
plt.figure(figsize=(10, 6))
for column in daily_avg_subTime:
    plt.plot(daily_avg_subTime.index, daily_avg_subTime[column], label=titles[cnt])
    cnt = cnt + 1
plt.title('WBA Daily Totals')
plt.minorticks_on()
plt.grid(b=bool, which='major', axis='both')
plt.ylabel('Number of people [N]')
plt.xticks(rotation=20)
plt.autoscale(enable=True, axis='x', tight=True)
plt.legend()  # legend in upper left side
plt.show()
plt.savefig(saveTSFig_path+'All_THs.png')
plt.close()

'''------------------------------------------DAILY STATS ON ALL THS--------------------------------------------------'''
daily_stats = pd.DataFrame({"Sum": daily_avg.sum(axis=1)})
daily_stats.insert(1, "Avg", daily_avg.mean(axis=1), True)
daily_stats.insert(2, "Median", daily_avg.median(axis=1), True)
daily_stats.insert(3, "Std", daily_avg.std(axis=1), True)
daily_stats.insert(4, "Max", daily_avg.max(axis=1), True)
daily_stats.insert(5, "Min", daily_avg.min(axis=1), True)
daily_stats.insert(6, "Range", daily_stats["Max"] - daily_stats["Min"], True)

daily_stats_subTime = daily_stats.loc['2020-12-1 01:00:00':'2021-3-20 04:00:00']
plt.figure()
#plt.scatter(daily_stats_subTime.index,daily_stats_subTime.Avg)
plt.errorbar(daily_stats_subTime.index, 'Sum', yerr='Range', data=daily_stats_subTime, fmt='o', color='black',
             ecolor='lightgray', elinewidth=3, capsize=0)
plt.show()

#fig1, ax1 = plt.subplots()
#ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
#ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
#plt.show()
