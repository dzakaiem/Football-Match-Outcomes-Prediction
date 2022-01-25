from selenium import webdriver
driver = webdriver.Chrome()
from collections import namedtuple
from operator import index
import pandas as pd
from sqlalchemy import column
df = pd.read_excel('/Users/danielzakaiem/Desktop/Football-Match-Outcomes-Prediction/ma_whole_df.xlsx')
print (df.head())


# add ELO column to df
Home_ELO_list = []
Away_ELO_list = []
URL_list = list(df ['Link'].values.tolist())

for URL in URL_list:
    driver.get(URL)    
    if URL == URL_list[0]:
        try:
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
    
    elif URL != URL_list[0]:
        try:
            ANALYSIS_button = driver.find_element_by_xpath('//*[@id="match"]/main/section[1]/div[1]/div/div/a[6]') #analysis button
            ANALYSIS_button.click()
            Home_ELO = driver.find_element_by_xpath('//*[@id="mod_team_analysis"]/div/div/div/table/tbody/tr[2]/td[1]/span').text
            print (Home_ELO)
            Away_ELO = driver.find_element_by_xpath('//*[@id="mod_team_analysis"]/div/div/div/table/tbody/tr[2]/td[3]/span').text
            print (Away_ELO)
            Home_ELO_list.append(Home_ELO)
            Away_ELO_list.append(Away_ELO)
        except:
            print ("An error had occurred")

# make the 2 new columns
df ['Home_ELO'] = Home_ELO_list 
df ['Away_ELO'] = Away_ELO_list
df_saved_in_excel = df.to_excel("newest_whole_df.xlsx", index = False)


# next step would be to add new potential features: cumulative goals scored this season, result of previous match, 


# add feature GSF (accumulated goals scored so far) - make the column names for GSF:

teams = (df['Home_Team'].unique()) # gives list of all seperate teams 

# make list for each team of "team-GSF"
column_names = [] # for GSF of each team
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

my_dict = { k: [] for k in teams} # key is the team, value is the list 
print (my_dict)  
for team , list in my_dict.items():
    for home_team, away_team, home_goals, away_goals in data_on_each_row:
        if home_team == team:
            if list:    
                list.append(list[-1] + home_goals) # cumulative, so must add to previous value for GSF
            else:
                list.append(home_goals) 
        elif away_team == team:
            if list:      # cumulative goals regardless of if scored home or away, so do same as above
                list.append (list[-1] + away_goals)
            else:
                list.append(away_goals)
        else:
            if list: 
                list.append(list[-1]) # add the previous fig if nothing has been added to accumulation of goals
            else:
                list.append(0)

# the 'values' in this dictionary are the lists to fill the columns!
for column_name, team in zip(actual_column_names,teams): #here, 'team' is essentially the key in the dictionary 
    df[column_name] = my_dict [team] 


df.to_excel("ma_whole_df_newest.xlsx", index = False) # new columns successfully added 