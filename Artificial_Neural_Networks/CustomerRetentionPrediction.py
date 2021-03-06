# -*- coding: utf-8 -*-
"""
used:
    https://machinelearningmastery.com/columntransformer-for-numerical-and-categorical-data/0

Created on Wed Apr  8 10:21:49 2020

@author: philipk01
"""
from sklearn.preprocessing import StandardScaler
import numpy as np

import pandas as pd
df = pd.read_csv('Churn_Modelling.csv')
pd.set_option('display.max_columns', None)

x = df.iloc[:, 3:13].values
y = df.iloc[:, 13].values

from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

#transformer = ColumnTransformer(transformers=[('cat', OneHotEncoder(drop='first'), [1, 2])], remainder='passthrough')
t = [('cat', OneHotEncoder(drop='first'), [1, 2]), ('num', StandardScaler(), [0, 3, 4, 5, 6, 7, 8, 9])]

transformer = ColumnTransformer(t, remainder='passthrough')

# transform training data
x = transformer.fit_transform(x)

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)


#############################################
######## K-Fold Validation - Sci-kit ########
#############################################
# BUILD MODEL
# combine Keras Sci-kit (Need Keras wrapper)
# Sequential model; to initialize ANN
from keras.models import Sequential
# Dense module to build ANN layers
from keras.layers import Dense # initializes weights

# Keras wrapper
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score

# need function, build classifier
# local classifier
def build_Classifier():
    classifier = Sequential() # ANN model
    classifier.add(Dense(units = 6, activation = 'relu', kernel_initializer = 'uniform', input_dim = 11))
    classifier.add(Dense(units = 6, activation = 'relu', kernel_initializer = 'uniform'))
    classifier.add(Dense(units = 1, activation = 'sigmoid', kernel_initializer = 'uniform'))
    classifier.compile(optimizer = 'Adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
    return classifier

# from keras.callbacks import ModelCheckpoint
# checkpoint = ModelCheckpoint("best_model.hdf5", monitor='loss', verbose=1, save_best_only=True, mode='auto', period=1)

# global classifier
classifier = KerasClassifier(build_fn = build_Classifier, batch_size = 10, epochs = 20)
accuracies = cross_val_score(estimator = classifier, X = x_train, y = y_train, cv = 10, n_jobs = -1)

# model accuracy
mean = accuracies.mean()
variance = accuracies.std()



print("mean: ", round(mean, 5) * 100, "%", "\nvariance: ", round(variance, 5), sep='')



# make predictions on new data
"""
predict if the customer with the following informations will leave the bank:

    Geography: France
    Credit Score: 600
    Gender: Male
    Age: 40 years old
    Tenure: 3 years
    Balance: $60000
    Number of Products: 2
    Does this customer have a credit card ? Yes
    Is this customer an Active Member: Yes
    Estimated Salary: $50000
    So should we say goodbye to that customer ?

"""

classifier.fit(x_train, y_train, batch_size = 10, epochs = 100)

# Predicting the Test set results
y_pred = classifier.predict(x_test)
y_pred = (y_pred > 0.5)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

# make prediction on the data above
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
new_prediction = classifier.model.predict(sc.fit_transform(np.array([0, 0, 600, 1,  40, 3, 60000, 2, 1, 1, 50000]).reshape(-1, x_test.shape[1])))

if (new_prediction > 0.60) > True:
    print("Client will remain with the bank with probability: ", round(new_prediction.reshape(1)[0] * 100, 2), "\%")
    
else:
    print("Client will leave bank with probability: ", round(100 - new_prediction.reshape(1)[0]* 100, 2),"%")
