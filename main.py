import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

df = pd.read_csv("C:/Users/tjmor/OneDrive/Documents/Consulting/UAC_beacon/WBA_data/BCC Bear Trap RAW.csv")

print(df.head(5))


df.plot(0, [1], subplots=False)