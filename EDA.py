from dis import show_code
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns 
import os



# step 1 - understanding the data
# lets start with oNLY using all the premier league oness:
data_set_names = os.listdir('/Users/danielzakaiem/Downloads/Football-Dataset/premier_league') # list of premier league names
print (data_set_names)

data_set_names = sorted(data_set_names) #puts list of data set names in order (from 1990-2021)
my_list = [] 
for data_set in data_set_names:
    my_list.append(pd.read_csv(f'/Users/danielzakaiem/Downloads/Football-Dataset/premier_league/{data_set}'))
    print (data_set)


#my_list is now a list of pd's whcih we must concatenate i think 

whole_df = pd.concat(my_list, ignore_index = True) # is the ENTIRE concatenated premier league datasets - added one below the other 

print (whole_df.head())
print(whole_df.tail())



# step 2 - cleaning the data - I HAVE DECIDED TO MAKE IT SO THAT THEMODEL PREDICTS 'WILL THE RESULT BE 'H' (HOME TEAM), 'A'(AWAY TEAM') OR 'D'(DRAW)

irrelevant_features = ['Link', 'Away_Team', 'League']
for feature in irrelevant_features:
    whole_df = whole_df.drop (feature, axis = 1) #drop irrelevant columns

# update result column values to '1' - home win , '2' - away win , '3' - draw
# i would have to do this by : for each row, split score in to 2 numbers and use eqaulity command to see winner:
count_row = whole_df.shape[0]  
print (count_row)      # Gives number of rows- which is 12417
#print (type(whole_df ['Result']))






whole_df ['Outcome'] = np.nan # make new column with null values

print (whole_df.tail()) # just to check out 

list_of_results= []

#'1' - home win , '2' - away win , '3' - draw
for x in range(12): #12417 rows appaz - change to this after...
   score = str(whole_df.loc[x,"Result"])
   print (score)  
   score_updated = score.split("-")
   home = int(score_updated[0])
   away = int(score_updated[1])
   print (f'The home team scored {home} goals')
   print (f'The away team scored {away} goals')
   if home > away:
    list_of_results.append(1)
   elif home < away:
     list_of_results.append(2)
   else:
       list_of_results.append(3)

print (list_of_results)
   




#print (whole_df.corr()) # useless as we only using it to find correlation of all the features with the target ('score') which can not be done here since 'score' isnt a plain number 
#print (whole_df.columns) # ascertain column is dropped 

#print (whole_df.isnull().sum()) # shows us how many null values per column- should be non in each



# step 3 - analysing relationship between variables ('features') - lets calculate the pearson correlation co-efficient between the variables to decdie on elimination?

#correlations_matrix =  (whole_df.corr()) #gives a matrix of ALL correlation co-efficients between each variable (mor eeffcient than dfinding them seperately no?)
#print (correlations_matrix.head()) #I THINK IT ONLY SHOWS BETWEEN SEASON AND ROUND COLUMNS (VARIABLES) AS THESE ONLY WITH SAME OBJECT TYPE TO COMPARE 


#first lets do analysis on 'season' and 'round' column:
#print (np.corrcoef(whole_df['Season'],whole_df['Round'])) # this method gets the correlation co-efficient in matrix form- so the r value is just -0.047...

#scatter_plot = sns.scatterplot(x = whole_df['Season'], y = whole_df ['Round']) # ovs basically shows the graph which has this specific 'r' value ^^^
# not sure comand to show this object^
#np.corrcoef(whole_df['Home_Team'], whole_df['Result']) # you cant find the correlation coefficient between a string column and an integer column  - this wont work 




