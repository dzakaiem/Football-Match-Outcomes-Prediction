import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns 
import os

# step 1 - understand the data

data_set_names = os.listdir('/Users/danielzakaiem/Downloads/Football-Dataset/premier_league') # list of premier league names
print (data_set_names)
data_set_names = sorted(data_set_names) 
my_list = [] 
for data_set in data_set_names:
    my_list.append(pd.read_csv(f'/Users/danielzakaiem/Downloads/Football-Dataset/premier_league/{data_set}'))
    print (data_set)

whole_df = pd.concat(my_list, ignore_index = True)  
print (whole_df.head())
print(whole_df.tail())


# step 2 - clean the data

irrelevant_features = ['League']
for feature in irrelevant_features:
    whole_df = whole_df.drop (feature, axis = 1)

whole_df['Index'] = np.arange(len(whole_df)) # add an index column 
whole_df.set_index('Index') 
print (whole_df.shape)
whole_df = whole_df.drop(whole_df.index[12293]) 
print (whole_df.shape)  

# derive and then add these 2 columns to df
Home_goals = []
Away_goals = []
list_of_results= []
#'1' - home win , '2' - away win , '3' - draw
for x in range(0, (len(whole_df)+1)):    
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
       list_of_results.append(1)
      elif home < away:
        list_of_results.append(2)
      else:
        list_of_results.append(3)

# add all these findings into new 'Outcome' column

whole_df['Outcome'] = list_of_results 
whole_df ['Home_goals'] = Home_goals
whole_df ['Away_goals'] = Away_goals

print (whole_df.tail())
print (whole_df.shape)

print (whole_df.info())
print (whole_df.describe())
print (whole_df.isnull().sum()) 
duplicate_rows = whole_df.duplicated()
print (duplicate_rows.sum())
# all seems good^

# remove outliers and replace with mode/mean 
print(whole_df.shape)
continuous_variables = ['Home_goals', 'Away_goals']
for variable in continuous_variables:
  whole_df.boxplot(column=[variable])
  plt.show()

def find_outlier(col): 
    sorted (col)
    lower_quartile, upper_quartile = col.quantile([0.25,0.75])
    IQR = upper_quartile - lower_quartile
    lowerRange = lower_quartile - (1.5 * IQR) 
    upperRange = upper_quartile + (1.5 * IQR) 
    return lowerRange, upperRange

for variable in continuous_variables:
    lowscore, highscore = find_outlier(whole_df[variable]) 
    whole_df[variable] = np.where(whole_df[variable] > highscore, highscore, whole_df[variable])
    whole_df[variable] = np.where(whole_df[variable] < lowscore, lowscore, whole_df[variable])

# should see that any outliers are removed
continuous_variables = ['Home_goals', 'Away_goals']
for variable in continuous_variables:
  whole_df.boxplot(column=[variable]) 
  plt.show()

print(whole_df.shape)

df_saved_in_excel = whole_df.to_excel("ma_whole_df.xlsx", index = False)


# step 3 - analysing relationship between variables 

print (whole_df.corr()) 
heat_map = sns.heatmap(whole_df.corr(), annot=True, cmap= 'RdYlGn')
plt.show()

columns = ['Season', 'Round']
for column in columns:
  plot = sns.regplot(x = column, y = 'Outcome', data=whole_df)
  plt.show()
