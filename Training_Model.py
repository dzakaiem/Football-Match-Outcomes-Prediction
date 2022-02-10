gitimport pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, mean_squared_error,r2_score
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import scale
from sklearn.tree import DecisionTreeClassifier 
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
import joblib
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix

df = pd.read_excel('/Users/danielzakaiem/Desktop/Football-Match-Outcomes-Prediction/ma_whole_df_newest.xlsx')
print (df.head())

X = df.drop(['Outcome'], axis = 1) 
y = df ['Outcome'] 
print (X.head())
print (y.head())

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2) 

X_test, X_validation, y_test, y_validation = train_test_split (X_test, y_test, test_size=0.3)
print ('Number of samples in:')
print (f'Training: {len(y_train)}')
print (f'Validation: {len(y_validation)}')
print (f'Testing: {len(y_test)}')

# try mutiple sk-learn models
models = [DecisionTreeClassifier(), SVC(), KNeighborsClassifier(), GaussianNB()] 
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

model = KNeighborsClassifier().fit(X_train, y_train) # best model 
joblib.dump(model, "model.joblib")

# tune the model 

search_space = {
    "weights" : ["uniform", "distance"],
    "algorithm" : ["auto", "ball_tree", "kd_tree", "brute"]
  }                      

GS = GridSearchCV(      
    estimator= model, 
    param_grid= search_space, 
    scoring= ["r2", "neg_root_mean_squared_error"], 
    refit = "r2",              # grid search object will return a model that is best with respect to the r2 matric 
    cv = 5,                     
    verbose = 1               
    )              

GS.fit (X_train, y_train) # 'optimal' model is made
print (GS.best_estimator_) # complete details of the best model (ie: best set of hyperparams)
print (GS.best_params_)  
print(GS.best_score_) 


KNN_pred = model.predict (X_test)
cm = confusion_matrix(y_test, KNN_pred)
print (cm)

# bring results to CSV file to 'fully' reflect results 
df = pd.DataFrame(GS.cv_results_)
df = df.sort_values ("rank_test_r2")
df.to_csv("cv_results.csv")


