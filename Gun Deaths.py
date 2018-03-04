
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

#first, seed df with 
#total gun deaths by race (#previously called 'race_counts')
#total population by race
#GD per 100k
  
gd_by_race = pd.DataFrame({'Total GD': df.groupby('race')['Indx'].count()}).reset_index()
gd_by_race['Total Pop'] = gd_by_race['race'].map(cen_race)
gd_by_race['GD per 100k'] = gd_by_race['Total GD'] / gd_by_race['Total Pop'] *100000

#then, create column for each method of intent, and compute GD per 100k:
for aim in df['intent'].unique():
    aim_df = pd.DataFrame({'GD': df[df['intent'] == aim].groupby('race')['Indx'].count()}).reset_index()
    gd_by_race[aim] = aim_df['GD'] / gd_by_race['Total Pop'] *100000

#drop Total GD column, and also a 'nan' column that tagged along:
summary_df = gd_by_race.drop(labels = ['Total GD', nan], axis=1)

#nplot this data
 #top 2

x_labels=['Asian','Black','Hispanic','Native Am','White']
d1 = summary_df['Suicide']
d2 = summary_df['Homicide']


plt.bar(ind,d1, color=(0.2588,0.4433,1.0), label = 'Suicide')
plt.bar(ind, d2, bottom = d1, color = (1.0,0.5,0.62), label = 'Homicide')
plt.legend()
plt.xticks(x_label,rotation=40)
plt.xlabel('Race')
plt.ylabel('Gun Deaths per 100,000')
plt.title('Gun Deaths per 100,000 by race')

#all of them
#sort first
#then do this:
colors = [] #fill in with non-obnxious colors
p_data = summary_df.drop(['race','GD per 100k'], axis=1)
d_col = p_data.columns
plt.bar(ind,p_data[d_col[0]], color=colors[0], label = d_col[0])
plt.bar(ind, p_data[d_col[x]], bottom = p_data[d_col[x-1]], color = colors[x], label = d_col[x])
plt.xticks(ind,x_labels, rotation =40)
plt.legend()
