# this file is solely to find new (potential) features to add to thhe previous:


#'ELO' ranking for each match can be found on each link under 'ANALYSIS' section on the left box- scrpe this feature as well as other you can find:

from selenium import webdriver
driver = webdriver.Chrome()
import pandas as pd
df = pd.read_excel('ma_whole_df.xlsx')
print (df.head())



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
        except:
            print ("An error had occurred")





#accept cookies button which pops up:



#change to 'ANALYSIS' by clicking on it


#find and grab 'ELO'


# now find a way to do this^ as an iteration for every link, then add columns for it (2 seperate colums)