# this file is solely to find new (potential) features to add to thhe previous:

#'ELO' ranking for each match can be found on each link under 'ANALYSIS' section on the left box- scrpe this feature as well as other you can find:

from selenium import webdriver
driver = webdriver.Chrome()
URL = 'https://www.besoccer.com/match/charlton-athletic-fc/derby-county-fc/19902727'
driver.get(URL) # all links autom. bring us to 'EVENTS' Tab


#accept cookies button which pops up:

try:
    cookies_agree_button = driver.find_element_by_xpath('//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')
    print (f'This button says "{cookies_agree_button.text}", and I have just pressed it for you')
    cookies_agree_button.click()
except:
    pass


#change to 'ANALYSIS' by clicking on it
try:
    ANALYSIS_button = driver.find_element_by_xpath('//*[@id="match"]/main/section[1]/div[1]/div/div/a[6]') #ANALYSIS BUTTON 
    ANALYSIS_button.click()
except:
    print ("This must not be the correct button")

#find and grab 'ELO'
Home_ELO = driver.find_element_by_xpath('//*[@id="mod_team_analysis"]/div/div/div/table/tbody/tr[2]/td[1]/span').text
print (Home_ELO)
Away_ELO = driver.find_element_by_xpath('//*[@id="mod_team_analysis"]/div/div/div/table/tbody/tr[2]/td[3]/span').text
print (Away_ELO)