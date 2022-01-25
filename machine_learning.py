from outcome import Outcome
import pandas as pd
import sklearn 


df = pd.read_excel('/Users/danielzakaiem/Desktop/Football-Match-Outcomes-Prediction/ma_whole_df_newest.xlsx')
print (df.head())
X = df.drop(['Outcome'], axis = 1)
y = df ['Outcome']
print (X.head())
print (y.head())