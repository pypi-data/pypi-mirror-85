This module is used to get metrics of Machine Learning/Deep Learning Models.It consists of all sklearn.metrics and stats module methods.Using this module you can also use all all different distances obtained in metrics.pairwise.cosine_distance etc.

from sklearning.metrics import *

y_test = [0,1,2,3,4]

y_pred = [0,1,2,3,5]

#Root Mean Squared Error

rmse = rootMeanSquaredError(y_test,y_pred)

print(rmse)

o/p:0.4472135954999579



#Regressor Summary

summary = regressorSummary(y_test,y_pred)

print(summary)

#Stats Value

statsValue(y_test,y_pred)

o/p:

statsValue(y_test,y_pred)

pvalues

 [0.53047777 0.00190127]

tvalues

 [-0.70710678 10.39230485]

rsquared

 0.972972972972973

rsquared_adj

 0.963963963963964


#All methods of sklean.metrics can be used by just giving the name of methods ex:

mse = mean_squared_error(y_test,y_pred)

print(mse)

o/p: 0.2