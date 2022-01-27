from outcome import Outcome
import pandas as pd
from sklearn import preprocessing
import numpy as np
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import scale
from sklearn.tree import DecisionTreeClassifier 
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
import joblib


df = pd.read_excel('/Users/danielzakaiem/Desktop/Football-Match-Outcomes-Prediction/ma_whole_df_newest.xlsx')
print (df.head())


X = df.drop(['Outcome'], axis = 1) # we need to make these continuous variables
y = df ['Outcome']  #and keep this at cetegorical
print (X.head())
print (y.head())

# we just standarize all column values into numbers (in order to apply machine learning to the dataset), EXCEPT from the target ('Outcome'), which stays categorical
# 
def preprocess_features(X):
    '''Converts all categorial variables into dummy varibles'''
    output = pd .DataFrame(index = X.index)
    for col,col_data in X.iteritems():
        if col_data.dtype == object:
            col_data = pd.get_dummies(col_data, prefix = col)
        
        output = output.join(col_data)
    
    return output

X = (preprocess_features(X)) # X is now columns all as integer object types  
print (X.tail())

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2) 

# first, standardize/normalize the data before feeding it to the model 

# but wait, lets also create a validation set , as we want to compare different models
# split the test test
X_test, X_validation, y_test, y_validation = train_test_split (X_test, y_test, test_size=0.3)
print ('Number of samples in:')
print (f'Training: {len(y_train)}')
print (f'Validation: {len(y_validation)}')
print (f'Testing: {len(y_test)}')

# try mutiple sk-learn models
# np.random.seed(2)

models = [DecisionTreeClassifier(), SVC(), KNeighborsClassifier(n_neighbors=5)] 
model_overview = []
for model in models:
    model.fit( X_train, y_train) # the model 

    y_test_pred = model.predict (X_test) # y prediction
    y_validation_prediction = model.predict (X_validation)
    
    test_loss = mean_squared_error (y_test , y_test_pred)
    validation_loss = mean_squared_error (y_validation, y_validation_prediction)
   
    test_accuracy = accuracy_score (y_test_pred, y_test)
    validaiton_accuracy = accuracy_score (y_validation, y_validation_prediction)
    
    model_overview.append(
     f"{model.__class__.__name__}: | Validation Loss: {validation_loss} | "
        f"Test Loss: {test_loss}"
    )

print (model_overview)

model = DecisionTreeClassifier().fit(X_train, y_train)
joblib.dump(model, "model.joblib")

#WAIT, I THOUGHT YOU HAVETO USE VALIDATION SET TO COMPARE MODELS?
# 'best' model is DecisionTreeClassifier - which we will use


