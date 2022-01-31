from outcome import Outcome
import pandas as pd
from sklearn import preprocessing
import numpy as np
import sklearn
from sklearn.metrics import accuracy_score, mean_squared_error,r2_score
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import scale
from sklearn.tree import DecisionTreeClassifier 
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
import joblib
from sklearn.model_selection import GridSearchCV

df = pd.read_excel('/Users/danielzakaiem/Desktop/Football-Match-Outcomes-Prediction/ma_whole_df_newest.xlsx')
print (df.head())


X = df.drop(['Outcome'], axis = 1) # we need to make these continuous variables
y = df ['Outcome']  #and keep this at cetegorical
print (X.head())
print (y.head())

# we just standarize all column values into numbers (in order to apply machine learning to the dataset), EXCEPT from the target ('Outcome'), which stays categorical

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

X_test, X_validation, y_test, y_validation = train_test_split (X_test, y_test, test_size=0.3)
print ('Number of samples in:')
print (f'Training: {len(y_train)}')
print (f'Validation: {len(y_validation)}')
print (f'Testing: {len(y_test)}')

# try mutiple sk-learn models

models = [DecisionTreeClassifier(), SVC(), KNeighborsClassifier(n_neighbors=5)] 
model_overview = []
for model in models:
    model.fit( X_train, y_train) 

    y_test_pred = model.predict (X_test) 
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

model = DecisionTreeClassifier().fit(X_train, y_train) # best model 
joblib.dump(model, "model.joblib")


# tune the model using the validation dataset 

search_space = {"criterion" : ["gini", "entropy"], "splitter" : ["best", "random"],"max_depth" : [1,2,3,4]} # search space 

# make grid search object
GS = GridSearchCV(estimator= model, 
param_grid= search_space, 
scoring= ["r2", "neg_root_mean_squared_error"], # will use these to score each model
refit = "r2",              #the grid search onjec will return a modle that is best with respect to the r2 matric 
cv = 5,                     # we wil be using 5 -fold cross vaidation 
verbose = 4)              # this rells us how mich infrmation we want to print 

GS.fit (X_train, y_train) # results of GS
print (GS.best_estimator_) # complete details of the best model (ie: best set of hyperparams)
print (GS.best_params_)  # to solely get best set of hyper params
print(GS.best_score_) # according to what you used in the refit method (r2 in this case)

# brings restults to CSV file to 'fully' reflect results 

df = pd.DataFrame(GS.cv_results_)
df = df.sort_values ("rank_test_r2")
df.to_csv("cv_results.csv")

# read over csv to come up woth a more efficient model - iterative process



