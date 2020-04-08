import pandas as pd
from sklearn.tree import DecisionTreeClassifier 
from sklearn.model_selection import train_test_split 
from sklearn import metrics
import numpy as np
import pickle


col_names = ['STEP','LAPV','TENG','LAPM','prevF','nextF','MV_STEP','ratio','trend','IMG_PATH','due']
# load dataset
album = pd.read_csv("album/album.csv", header=0, names=col_names)


album['due'].replace({'small':0, 'big':1}, inplace=True)
album['trend'].replace({'down':0, 'up':1}, inplace=True)


feature_cols = ['LAPV','TENG','LAPM','prevF','nextF','ratio', 'trend']

X = album[feature_cols] # Features
y = album.due # Target 

# 90% training and 10% test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=1) 


clf = DecisionTreeClassifier()
# Train Decision Tree Classifer
clf = clf.fit(X_train,y_train)
#Predict the response for test dataset
y_pred = clf.predict(X_test)


filename = 'modelo.sav'

pickle.dump(clf, open(filename, 'wb'))
print("MODEL SAVED")  
