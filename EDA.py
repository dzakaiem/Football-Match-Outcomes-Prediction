from dis import show_code
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns 
import os
from sqlalchemy import true

# step 1 - understanding the data
# start with only data for premier league

data_set_names = os.listdir('/Users/danielzakaiem/Downloads/Football-Dataset/premier_league') # list of premier league names
print (data_set_names)
data_set_names = sorted(data_set_names) # puts list of data set names in order (from 1990-2021)
my_list = [] 
for data_set in data_set_names:
    my_list.append(pd.read_csv(f'/Users/danielzakaiem/Downloads/Football-Dataset/premier_league/{data_set}'))
    print (data_set)

whole_df = pd.concat(my_list, ignore_index = True) # ENTIRE concatenated premier league datasets - added one below the other 
print (whole_df.head())
print(whole_df.tail())


# step 2 - cleaning the data 

irrelevant_features = ['League']
for feature in irrelevant_features:
    whole_df = whole_df.drop (feature, axis = 1) # drop irrelevant columns

whole_df ['Outcome'] = np.nan # make new column with null values

whole_df['Index'] = np.arange(len(whole_df)) # add an index column 
whole_df.set_index('Index') 
print (whole_df.shape)
whole_df = whole_df.drop(whole_df.index[12293]) # this should drop row with index 12293 (the 'error' row)
print (whole_df.shape)  

Home_goals = []
Away_goals = []
list_of_results= []
#'1' - home win , '2' - away win , '3' - draw
for x in range(0, (len(whole_df)+1)):    # remember , row 12293 is non existant anymore - index skips from 12292 to 12294
    if x != 12293:
      score = str(whole_df.loc[x,"Result"])
      print (score)  
      score_updated = score.split("-")
      Home_goals.append (int(score_updated[0]))
      Away_goals.append (int(score_updated[1]))
      print (score_updated)
      home = int(score_updated[0])
      away = int(score_updated[1])
      print (f'The home team scored {home} goals')
      print (f'The away team scored {away} goals') 
      if home > away:
       list_of_results.append('1')
      elif home < away:
        list_of_results.append('2')
      else:
        list_of_results.append('3')



# now we need to add all these results into new 'Outcome' column

whole_df['Outcome'] = list_of_results # add these 3 new columns
whole_df ['Home_goals'] = Home_goals
whole_df ['Away_goals'] = Away_goals

print (whole_df.tail())

df_saved_in_excel = whole_df.to_excel("ma_whole_df.xlsx", index = False)



# step 3 - analysing relationship between variables ('features') - lets calculate the pearson correlation co-efficient between the variables to decdie on elimination?

print (whole_df.corr()) 





