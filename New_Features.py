from pyexpat import features
import pandas as pd
import time
import matplotlib.pyplot as plt 
import numpy as np
import seaborn as sns
from time import time
from selenium import webdriver

driver = webdriver.Chrome()


df = pd.read_excel('/Users/danielzakaiem/Desktop/Football-Match-Outcomes-Prediction/ma_whole_df.xlsx')
print (df.head())
print (len(df))

# add ELO column to df
Home_ELO_list = []
Away_ELO_list = []
URL_list = list(df['Link'].values.tolist()) 
x = df.drop('Link', inplace = True, axis=1) # not needed column anymore
print(df.head())

for URL in URL_list:
    driver.get(URL)    
    pop_up = driver.find_element_by_xpath('//*[@id="grv-popup__subscribe"]') # pop up button
    if URL == URL_list[0]:
        try:
            time.sleep(10)
            pop_up = driver.find_element_by_xpath('//*[@id="grv-popup__subscribe"]') # pop up button 
            pop_up.click()
            cookies_agree_button = driver.find_element_by_xpath('//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')
            print (f'This button says "{cookies_agree_button.text}", and I have just pressed it for you')
            cookies_agree_button.click()
            ANALYSIS_button = driver.find_element_by_xpath('//*[@id="match"]/main/section[1]/div[1]/div/div/a[6]') # analysis button
            ANALYSIS_button.click()
            Home_ELO = driver.find_element_by_xpath('//*[@id="mod_team_analysis"]/div/div/div/table/tbody/tr[2]/td[1]/span').text
            print (Home_ELO)
            Away_ELO = driver.find_element_by_xpath('//*[@id="mod_team_analysis"]/div/div/div/table/tbody/tr[2]/td[3]/span').text
            print (Away_ELO)
            Home_ELO_list.append(Home_ELO)
            Away_ELO_list.append(Away_ELO)
        except:
            print ("An error had occurred")
    
    elif URL != URL_list[0]: # rest of the URL's after the first
        try:
            pop_up.click()
            ANALYSIS_button = driver.find_element_by_xpath('//*[@id="match"]/main/section[1]/div[1]/div/div/a[6]') #analysis button
            ANALYSIS_button.click()
            Home_ELO_list.append(driver.find_element_by_xpath('//*[@id="mod_team_analysis"]/div/div/div/table/tbody/tr[2]/td[1]/span').text)
            Away_ELO_list.append(driver.find_element_by_xpath('//*[@id="mod_team_analysis"]/div/div/div/table/tbody/tr[2]/td[3]/span').text)
        except:
            print ("An error had occurred")

# make the 2 new columns
df ['Home_ELO'] = Home_ELO_list 
df ['Away_ELO'] = Away_ELO_list
# df_saved_in_excel = df.to_excel("newest_whole_df.xlsx", index = False)


# add feature GSF (accumulated goals scored so far)
teams = (df['Home_Team'].unique()) 
column_names = [] 
for team in teams:
    column_names.append(team + '_GSF') 
    
actual_column_names = []
for name in column_names:
    name = name.replace(" ", "_")  
    print (type(name))
    actual_column_names.append(name)

home_team_column = list(df['Home_Team']) # strings
away_team_column = list(df ['Away_Team']) 
home_goals_column= list(df['Home_goals']) # integers
away_goals_column = list (df['Away_goals'])
data_on_each_row = (list(zip(home_team_column, away_team_column, home_goals_column, away_goals_column)))

my_dict = { k: [] for k in teams}  
print (my_dict)  
for team , list in my_dict.items():
    for home_team, away_team, home_goals, away_goals in data_on_each_row:
        if home_team == team:
            if list:    
                list.append(list[-1] + home_goals) 
            else:
                list.append(home_goals) 
        elif away_team == team:
            if list:      
                list.append (list[-1] + away_goals)
            else:
                list.append(away_goals)
        else:
            if list: 
                list.append(list[-1]) 
            else:
                list.append(0)

# the 'values' in this dictionary are the lists to fill the columns!
for column_name, team in zip(actual_column_names, teams): 
    df[column_name] = my_dict[team] 

print (df.tail())
print (df.columns) # successfully added 

#  clean new features added

print(df.head())
print (df.shape)
print (df.info())
print (df.describe())
print (df.isnull().sum()) # no nulls resent
duplicate_rows = df.duplicated() # no duplicate rows present 
print (duplicate_rows.sum()) 

# handling outliers for newly added features
x = ['Home_ELO', 'Away_ELO']
new_features = x + actual_column_names  # all newly added columns
for feature in new_features:
    df.boxplot(column= feature)
    plt.show()
def eiliminate_outliers(col): 
    sorted (col)
    lower_quartile, upper_quartile = col.quantile([0.25,0.75])
    IQR = upper_quartile - lower_quartile
    lowerRange = lower_quartile - (1.5 * IQR) # value cannot be below this
    upperRange = upper_quartile + (1.5 * IQR) # or above this - outlier
    return lowerRange, upperRange
for feature in new_features:
    lowscore, highscore = eiliminate_outliers(df[feature])
    df[feature] = np.where(df[feature]>highscore,highscore, df[feature])
    df[feature] = np.where(df[feature]<lowscore, lowscore, df[feature])
df.boxplot(column=['Happiness Score']) # show it outliers been removed now
plt.show()

print (df.corr)
heat_map = sns.heatmap(df.corr(), annot=True,cmap= 'RdYlGn')
plt.show()
for column_name in new_features:   # show relation of y with new features
    sns.regplot(x= column_name ,y='Outcome', data=df)
    plt.show()

# last round of dropping out irrelevant columns - before feeding to model
df.drop(columns=['Home_Team', 'Away_Team', 'Result', 'Link', 'Index', 'Home_goals', 'Away_goals'], inplace=True)
print (df.corr)

# scale features before machine learning 

cols_to_norm =  df.columns.values.tolist()
cols_to_norm.remove('Outcome')
print(cols_to_norm)
df[cols_to_norm] = df[cols_to_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
print (df.tail())


df.to_excel("ma_whole_df_newest.xlsx", index = False) # new columns successfully added 
