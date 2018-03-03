
# coding: utf-8

# In[12]:


import pandas as pd
import datetime

df = pd.read_csv('guns.csv')
df.head()

df =df.rename(columns={'Unnamed: 0': 'Indx'})

#gun deaths by year (no change from 2012 --> 2014)
year_counts = df.groupby('year')['Indx'].count()

#create column that combine 'year' and 'month' column into one date-time object
df['dates'] = df.apply(lambda row: datetime.datetime(year = row['year'], month=row['month'], day=1), axis=1)


date_counts = df.groupby('dates')['Indx'].count()


#GD by sex, race:
sex_counts = df.groupby('sex')['Indx'].count()
race_counts = df.groupby('race')['Indx'].count()

    # Most are male
    # Most are white. 2nd most Black

'''skip to cen_race dictonary below
    #normalize to population by race:
    #*** csv file was pre-loaded into Jupyter notebook. I downloaded as tab-text file. So import needs tweaking if going to run here
    census = pd.read_csv('census.csv')
    census.head()
    
    #stupidly create a dictionary by hand of this data:
    cen_race = {'Asian/Pacific Islander': (census.loc[0,'Race Alone - Asian'] + census.loc[0, 'Race Alone - Native Hawaiian and Other Pacific Islander']),
            'White': census.loc[0,'Race Alone - White'],
                'Black': census.loc[0,'Race Alone - Black or African American'],
                'Native American/Native Alaskan': census.loc[0,'Race Alone - American Indian and Alaska Native'],
                'Hispanic': census.loc[0,'Race Alone - Hispanic']}
'''

cen_race = {'Asian/Pacific Islander': 15834141,
 'Black': 40250635,
 'Hispanic': 44618105,
 'Native American/Native Alaskan': 3739506,
 'White': 197318956}


#create a dataframe to look at gun deaths by rate per 100k total pop:
    #re-run 'race_counts' groupby from above, seed new DF with this
race_per_hundredk = pd.DataFrame({'GD': df.groupby('race')['Indx'].count()}).reset_index()
race_per_hundredk['Total Pop'] = race_per_hundredk['race'].map(cen_race)
race_per_hundredk['GD per 100k'] = race_per_hundredk['GD'] / race_per_hundredk['Total Pop'] * 100000
race_per_hundredk


#filter gun deaths for intent:

hom_race_counts = df[df['intent'] == 'Homicide'].groupby('race')['Indx'].count()
    #make into a df:
new_df = pd.DataFrame({'race' : hom_race_counts.index, 'hom GD': hom_race_counts.values})
    #merge with old df & do math
hom_race_per_hundk = pd.merge(race_per_hundredk, new_df, how = 'inner', left_on=['race'],right_on=['race'])
hom_race_per_hundk['hom GD per 100k'] = hom_race_per_hundk['hom GD'] / hom_race_per_hundk['Total Pop'] * 100000


#look at suicides, combine into 1 df:
suic_df = pd.DataFrame({'GD': df[df['intent'] == 'Suicide'].groupby('race')['Indx'].count()}).reset_index()
race_per_hundredk['suicide GD per 100k'] = suic_df['GD'] / race_per_hundredk['Total Pop'] *100000
race_per_hundredk['homicide GD per 100k'] = hom_race_per_hundk['hom GD per 100k']
