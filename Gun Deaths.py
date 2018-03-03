
import pandas as pd
import datetime

df = pd.read_csv('guns.csv')
df.head()

df =df.rename(columns={'Unnamed: 0': 'Indx'})


#want to normalize to population by race
#raw data from census data, manually loaded into a dictionary, for convenience:
cen_race = {'Asian/Pacific Islander': 15834141,
 'Black': 40250635,
 'Hispanic': 44618105,
 'Native American/Native Alaskan': 3739506,
 'White': 197318956}


#want to look at Gun Deaths, by race, by each different cause of death

#first, seed df with total gun deaths by race:
    #previously called 'race_counts'
gd_by_race = pd.DataFrame({'Total GD': df.groupby('race')['Indx'].count()}).reset_index()

#then, create column for each method of intent, and compute GD per 100k:
for int in df['intent'].unique():
    gd_by_race[int] = gd_by_race['Total GD'] / gd_by_race['race'].map(cen_race) * 100000

#drop Total GD column, and also a 'nan' column that tagged along:
summary_df = gd_by_race.drop(labels = ['Total GD', nan], axis=1)

#next: figure out a way to plot this data
