# this file is solely to find new (potential) features to add to thhe previous:


#'ELO' ranking for each match can be found on each link under 'ANALYSIS' section on the left box- scrpe this feature as well as other you can find:

# from selenium import webdriver
# driver = webdriver.Chrome()
from collections import namedtuple
from operator import index
import pandas as pd
from sqlalchemy import column
df = pd.read_excel('/Users/danielzakaiem/Desktop/Football-Match-Outcomes-Prediction/ma_whole_df.xlsx')
print (df.head())




# to add ELO column to df:
Home_ELO_list = []
Away_ELO_list = []
URL_list = list(df ['Link'].values.tolist())

for URL in URL_list:
    driver.get(URL)    # it seems cookies button only pops up for first one , not the rest after
    if URL == URL_list[0]:
        try:
            cookies_agree_button = driver.find_element_by_xpath('//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')
            print (f'This button says "{cookies_agree_button.text}", and I have just pressed it for you')
            cookies_agree_button.click()
            ANALYSIS_button = driver.find_element_by_xpath('//*[@id="match"]/main/section[1]/div[1]/div/div/a[6]') #ANALYSIS BUTTON 
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
            ANALYSIS_button = driver.find_element_by_xpath('//*[@id="match"]/main/section[1]/div[1]/div/div/a[6]') #ANALYSIS BUTTON 
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




# goals so far:


#make the column names for GSF:

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







    
    
# actual_column_names = 

# Charlton_Athletic_GSF 
# Tottenham_Hotspur_GSF
# Southampton_GSF
# Sheffield_Wednesday_GSF
# Queens_Park_Rangers_GSF
# Nottingham_Forest_GSF
# Man._Utd_GSF
# Liverpool_GSF
# Coventry_City_GSF
# Wimbledon_FC_GSF
# Arsenal_GSF
# Millwall_GSF
# Luton_Town_GSF
# Everton_GSF
# Crystal_Palace_GSF
# Chelsea_GSF
# Aston_Villa_GSF
# Derby_County_GSF
# Man._City_GSF
# Norwich_City_GSF
# Sheffield_United_GSF
# Leeds_United_GSF
# Sunderland_GSF
# West_Ham_GSF
# Notts_County_GSF
# Oldham_Athletic_AFC_GSF
# Ipswich_Town_GSF
# Blackburn_Rovers_GSF
# Middlesbrough_GSF
# Newcastle_GSF
# Swindon_Town_GSF
# Leicester_GSF
# Bolton_Wanderers_GSF
# Barnsley_GSF
# Watford_GSF
# Bradford_City_GSF
# Fulham_GSF
# Birmingham_City_GSF
# West_Bromwich_Albion_GSF
# Portsmouth_GSF
# Wolves_GSF
# Wigan_Athletic_GSF
# Reading_GSF
# Hull_City_GSF
# Stoke_City_GSF
# Burnley_GSF
# Blackpool_GSF
# Swansea_City_GSF
# Cardiff_City_GSF
# AFC_Bournemouth_GSF
# Brighton_&_Hove_Albion_GSF
# Huddersfield_Town_GSF


#STILL HAVENT FIGURED OUT HOW, BUT NEED TO MAKE THESE STRINGS^ INTO SEPERATE LISTS ( WHICH IS HARD COS U USUALLY ASSIGN A VARIABLE NAME TO = [], NOT A STRING )
# SO COME BACK TO THIS LATER^

# #lets try filling out one of these oclumns - solely for arsenal:
# Ars_GSF = []  # once cell above is fixed, we can refer to this list and other team's lists in a for loop
# home_team_column = list(df['Home_Team']) # strings
# away_team_column = list(df ['Away_Team']) 
# home_goals_column= list(df['Home_goals']) # integers
# away_goals_column = list (df['Away_goals'])
# data_on_each_row = (list(zip(home_team_column, away_team_column, home_goals_column, away_goals_column)))


# 
# for home_team, away_team, home_goals, away_goals in data_on_each_row:
#     if home_team == 'Arsenal':
#         if Ars_GSF[-1]:    # if there is already a stat for 'GOALS SO FAR', then we add to it (as it is cummulative). [-1] = 'last element in list'
#             Ars_GSF.append(Ars_GSF[-1] + home_goals) # add previous number pf GSF (as its accumulated)
#         else:
#             Ars_GSF.append(home_goals) # if no value before, then add this as the 'first' value in the list
#     elif away_team == 'Arsenal':
#         if Ars_GSF[-1]:      # and then do exactly the same ^, but it is just for home goals (which doesnt make a difference- this is goals scored regardless of at home or away)
#             Ars_GSF.append (Ars_GSF[-1] + away_goals)
#         else:
#             Ars_GSF.append(away_goals)
#     else:
#         if Ars_GSF: 
#             Ars_GSF.append(Ars_GSF[-1]) # add the previous fig if nothing has been added to accumulation of goals
#         else:
#             Ars_GSF.append(0)
            

# df ['Arsenal_GSF'] = Ars_GSF # add accumulated goals so far for arsenal 
# print (df.tail())
















# below is more efficient than version above^. ascertain correctness, then eliminate code above

home_team_column = list(df['Home_Team']) # strings
away_team_column = list(df ['Away_Team']) 
home_goals_column= list(df['Home_goals']) # integers
away_goals_column = list (df['Away_goals'])
data_on_each_row = (list(zip(home_team_column, away_team_column, home_goals_column, away_goals_column)))



my_dict = { k: [] for k in teams} # now, add the list of accumulated goals to each of the values in this dictionary
print (my_dict)  
for team , list in my_dict.items():
    for home_team, away_team, home_goals, away_goals in data_on_each_row:
        if home_team == team:
            if list:    # if there is already a stat for 'GOALS SO FAR', then we add to it (as it is cummulative). [-1] = 'last element in list'
                list.append(list[-1] + home_goals) # add previous number pf GSF (as its accumulated)
            else:
                list.append(home_goals) # if no value before, then add this as the 'first' value in the list
        elif away_team == team:
            if list:      # and then do exactly the same ^, but it is just for home goals (which doesnt make a difference- this is goals scored regardless of at home or away)
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
print (df.tail())



