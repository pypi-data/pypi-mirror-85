# Module name: umaat-Ultimate Machiene-learning Algorithm Accuracy Test
# Short description: umaat (or) Ultimate Machiene-learning Algorithm Accuracy Test  is a package that houses the  functions which can produce accuracy results for each algorithm in the categories of  Clustering,Regression & Classification based on passing the arguments - independent and dependent variables/features
# Advantage:The result from this algorithm gives the user of choice to choose the best  algorithm  for their dataset based on the accuracy produced
# Developers:  Vishal Balaji Sivaraman (@The-SocialLion) 
# Contact email address: vb.sivaraman_official@yahoo.com 
# Modules required: numpy,pandas,matplotlib,Scikit

# Command to install umaat:
# >>> pip install umaat

# IMPORTING REQUIRED MODULES
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from time import sleep

# Program/Source Code:
# X denotes all the independent features in a dataset
# Y denotes all the dependent features in a dataset
# Note: Data preprocessing is not involved in the dataset also test dataset cant be attached here but will soon bring it in an update

class model_accuracy:
  def accuracy_test(self,X,Y):
    from sklearn.model_selection import train_test_split
    print("WELCOME TO MACHIENE LEARNING - ALGORITHM  ACCURACY TEST")
    print("\nAccuracy is calculated for 1)Regression,2)Classification 3)Clustering Models( Currently Work in Progress)")
    i=int(input("Enter your Choice"))
    print("\nOnce the result is displayed the user can choose their desired algorithm for constructing their finished model")
    print("\n Note: No datapreprocessing is involved in this process ")
    print("\n If incase if u need to preprocess your data then for the upcoming filed type 0")
    o=float(input("enter test size for computation of accuracy of all the possible ml algorithms"))
    print("\n Generating train & test datasets for the given data..")
    X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = o, random_state = 0)
    print("\n Completed the genration of train and test datasets for the given data")
    if i==1: 
       print("REGRESSION ALGORITHM ACCURACY TEST!")
       Regressor_accuracy(X_train, X_test, y_train, y_test)
    elif i==2:
       print("CLAFFICATION ALGORITHM ACCURACY TEST!")
       Classifier_accuracy(X_train, X_test, y_train, y_test)

def Regressor_accuracy(X_train, X_test, y_train, y_test):
  print("\nLoading all the possible Regression models ")
  print("\nLoading completed.. ")
  print("\nTesting Accuracy for all the possible Regression models")
  print("\n please fill the details with care when prompted to avoid errors")
  for i in range(21):
     sys.stdout.write('\r')
     sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
     sys.stdout.flush()
     sleep(0.25)
  a1,b1,c1,d1,e1,f1=linear_reg(X_train,y_train,X_test,y_test)
  a2,b2,c2,d2,e2,f2=poly_reg(X_train,y_train,X_test,y_test)
  print("\n........Loading.........")
  print("\n This might take some couple of minutes due to bulk nature of the algorithm")
  print("\n Kindly do bear")
  a3,b3,c3,d3,e3,f3=svr_linear(X_train,y_train,X_test,y_test)
  a4,b4,c4,d4,e4,f4=svr_poly(X_train,y_train,X_test,y_test)
  print("\n.........LOADING.......")
  a5,b5,c5,d5,e5,f5=svr_rbf(X_train,y_train,X_test,y_test)
  a6,b6,c6,d6,e6,f6=svr_sig(X_train,y_train,X_test,y_test)
  a7,b7,c7,d7,e7,f7=decision_reg(X_train,y_train,X_test,y_test)
  a8,b8,c8,d8,e8,f8=random_reg(X_train,y_train,X_test,y_test)
  print("\nAccuracy results are in !.")
  print("\nGenerating Dataframe for the same..")
  for i in range(21):
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()
    sleep(0.25)
  print("\nNote: For any 2 columns it should assumed that the Linear Regression would be a Simple Linear Regression which means that for multiple columns the Linear Regression would be a multiple Linear Regression")
  print("\n Note: Incase if the Error , deviance values are high please use data preprocessing tools to scale down the value of the feature and try to run the algorithm again")
  data = {'Type of Regression':['Linear Regression', 'Polynomial Regression', 'Support Vector Regression(kernel="linear")','Support Vector Regression(kernel="poly")','Support Vector Regression(kernel="rbf")','Support Vector Regression(kernel="sigmoid")','Decision Tree Regression','Random Forest regression'], 'R2_score':[a1,a2,a3,a4,a5,a6,a7,a8],'Variance_score':[b1,b2,b3,b4,b5,b6,b7,b8],'Max_Error':[c1,c2,c3,c4,c5,c6,c7,c8],'Mean Absolute Error':[d1,d2,d3,d4,d5,d6,d7,d8],'Mean Squared Error':[e1,e2,e3,e4,e5,e6,e7,e8],'Median Absolute Error':[f1,f2,f3,f4,f5,f6,f7,f8]} 
  df = pd.DataFrame(data) 
  display(df)

def linear_reg(X_train,y_train,X_test,y_test):
  from sklearn.linear_model import LinearRegression
  from sklearn.metrics import r2_score,explained_variance_score,max_error,mean_absolute_error,mean_squared_log_error,mean_squared_error,median_absolute_error,mean_poisson_deviance,mean_gamma_deviance,mean_tweedie_deviance
  regressor = LinearRegression()
  regressor.fit(X_train, y_train)
  y_pred = regressor.predict(X_test)
  f1=(abs(r2_score(y_test,y_pred))*100)
  f2=(abs(explained_variance_score(y_test, y_pred))*100)
  f3=(abs(max_error(y_test, y_pred)))
  f4=(abs(mean_absolute_error(y_test, y_pred)))
  f5=(abs(mean_squared_error(y_test, y_pred)))
  f6=(abs(median_absolute_error(y_test, y_pred)))
  return f1,f2,f3,f4,f5,f6


def poly_reg(X_train,y_train,X_test,y_test):
  from sklearn.preprocessing import PolynomialFeatures
  from sklearn.linear_model import LinearRegression
  from sklearn.metrics import r2_score,explained_variance_score,max_error,mean_absolute_error,mean_squared_log_error,mean_squared_error,median_absolute_error,mean_poisson_deviance,mean_gamma_deviance,mean_tweedie_deviance
  p=int(input("Enter Degree of Polyniomial for Polynomial Regression"))
  poly_reg = PolynomialFeatures(degree = p)
  X_poly = poly_reg.fit_transform(X_train)
  regressor = LinearRegression()
  regressor.fit(X_poly, y_train)
  y_pred = regressor.predict(poly_reg.fit_transform(X_test))
  f1=(abs(r2_score(y_test,y_pred))*100)
  f2=(abs(explained_variance_score(y_test, y_pred))*100)
  f3=(abs(max_error(y_test, y_pred)))
  f4=(abs(mean_absolute_error(y_test, y_pred)))
  f5=(abs(mean_squared_error(y_test, y_pred)))
  f6=(abs(median_absolute_error(y_test, y_pred)))
  return f1,f2,f3,f4,f5,f6

def svr_linear(X_train,y_train,X_test,y_test):
  from sklearn.svm import SVR
  from sklearn.metrics import r2_score,explained_variance_score,max_error,mean_absolute_error,mean_squared_log_error,mean_squared_error,median_absolute_error,mean_poisson_deviance,mean_gamma_deviance,mean_tweedie_deviance
  regressor= SVR(kernel = 'linear')
  regressor.fit(X_train, y_train)
  y_pred = regressor.predict(X_test)
  f1=(abs(r2_score(y_test,y_pred))*100)
  f2=(abs(explained_variance_score(y_test, y_pred))*100)
  f3=(abs(max_error(y_test, y_pred)))
  f4=(abs(mean_absolute_error(y_test, y_pred)))
  f5=(abs(mean_squared_error(y_test, y_pred)))
  f6=(abs(median_absolute_error(y_test, y_pred)))
  return f1,f2,f3,f4,f5,f6

def svr_poly(X_train,y_train,X_test,y_test):
  from sklearn.svm import SVR
  from sklearn.metrics import r2_score,explained_variance_score,max_error,mean_absolute_error,mean_squared_log_error,mean_squared_error,median_absolute_error,mean_poisson_deviance,mean_gamma_deviance,mean_tweedie_deviance
  regressor = SVR(kernel = 'poly')
  regressor.fit(X_train, y_train)
  y_pred = regressor.predict(X_test)
  f1=(abs(r2_score(y_test,y_pred))*100)
  f2=(abs(explained_variance_score(y_test, y_pred))*100)
  f3=(abs(max_error(y_test, y_pred)))
  f4=(abs(mean_absolute_error(y_test, y_pred)))
  f5=(abs(mean_squared_error(y_test, y_pred)))
  f6=(abs(median_absolute_error(y_test, y_pred)))
  return f1,f2,f3,f4,f5,f6

def svr_rbf(X_train,y_train,X_test,y_test):
  from sklearn.svm import SVR
  from sklearn.metrics import r2_score,explained_variance_score,max_error,mean_absolute_error,mean_squared_log_error,mean_squared_error,median_absolute_error,mean_poisson_deviance,mean_gamma_deviance,mean_tweedie_deviance
  regressor = SVR(kernel = 'rbf')
  regressor.fit(X_train, y_train)
  y_pred = regressor.predict(X_test)
  f1=(abs(r2_score(y_test,y_pred))*100)
  f2=(abs(explained_variance_score(y_test, y_pred))*100)
  f3=(abs(max_error(y_test, y_pred)))
  f4=(abs(mean_absolute_error(y_test, y_pred)))
  f5=(abs(mean_squared_error(y_test, y_pred)))
  f6=(abs(median_absolute_error(y_test, y_pred)))
  return f1,f2,f3,f4,f5,f6

def svr_sig(X_train,y_train,X_test,y_test):
  from sklearn.svm import SVR
  from sklearn.metrics import r2_score,explained_variance_score,max_error,mean_absolute_error,mean_squared_log_error,mean_squared_error,median_absolute_error,mean_poisson_deviance,mean_gamma_deviance,mean_tweedie_deviance
  regressor = SVR(kernel = 'sigmoid')
  regressor.fit(X_train, y_train)
  y_pred = regressor.predict(X_test)
  f1=(abs(r2_score(y_test,y_pred))*100)
  f2=(abs(explained_variance_score(y_test, y_pred))*100)
  f3=(abs(max_error(y_test, y_pred)))
  f4=(abs(mean_absolute_error(y_test, y_pred)))
  f5=(abs(mean_squared_error(y_test, y_pred)))
  f6=(abs(median_absolute_error(y_test, y_pred)))
  return f1,f2,f3,f4,f5,f6

def decision_reg(X_train,y_train,X_test,y_test):
  from sklearn.tree import DecisionTreeRegressor
  from sklearn.metrics import r2_score,explained_variance_score,max_error,mean_absolute_error,mean_squared_log_error,mean_squared_error,median_absolute_error,mean_poisson_deviance,mean_gamma_deviance,mean_tweedie_deviance
  regressor = DecisionTreeRegressor(random_state = 0)
  regressor.fit(X_train, y_train)
  y_pred = regressor.predict(X_test)
  f1=(abs(r2_score(y_test,y_pred))*100)
  f2=(abs(explained_variance_score(y_test, y_pred))*100)
  f3=(abs(max_error(y_test, y_pred)))
  f4=(abs(mean_absolute_error(y_test, y_pred)))
  f5=(abs(mean_squared_error(y_test, y_pred)))
  f6=(abs(median_absolute_error(y_test, y_pred)))
  return f1,f2,f3,f4,f5,f6

def random_reg(X_train,y_train,X_test,y_test):
  from sklearn.ensemble import RandomForestRegressor
  from sklearn.metrics import r2_score,explained_variance_score,max_error,mean_absolute_error,mean_squared_log_error,mean_squared_error,median_absolute_error,mean_poisson_deviance,mean_gamma_deviance,mean_tweedie_deviance
  t=int(input("Enter number of trees for random forest regression"))
  regressor = RandomForestRegressor(n_estimators = t, random_state = 0)
  regressor.fit(X_train, y_train)
  y_pred = regressor.predict(X_test)
  f1=(abs(r2_score(y_test,y_pred))*100)
  f2=(abs(explained_variance_score(y_test, y_pred))*100)
  f3=(abs(max_error(y_test, y_pred)))
  f4=(abs(mean_absolute_error(y_test,y_pred)))
  f5=(abs(mean_squared_error(y_test, y_pred)))
  f6=(abs(median_absolute_error(y_test, y_pred)))
  return f1,f2,f3,f4,f5,f6

def Classifier_accuracy(X_train, X_test, y_train, y_test):
  d=int(input("enter the number of unique classes present in your dataset"))
  b=[]
  for i in range (d):
    c=input("enter the different classes in any order")
    b.append(c)
  print("\nClasses are",b)
  print("\n Note: any non negative number is fine for the below field and it need not be the number of classes/categories in the  dataset")
  a=int(input("enter the number of labels for calculation of score"))
  l=int(input("Enter the value of beta for calculation of score"))
  print("\nLoading all the possible Classification  models ")
  print("\nLoading completed.. ")
  print("\nTesting Accuracy for all the possible Classification models")
  print("\n please fill the details with care when prompted to avoid errors")
  for i in range(21):
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()
    sleep(0.25)
  a1,b1,c1,d1,e1,f1,g1,h1,i1,j1,k1,l1,m1,n1,o1,p1,q1,r1,s1=log_reg(X_train,y_train,X_test,y_test,a,l)
  n,j,s,a2,b2,c2,d2,e2,f2,g2,h2,i2,j2,k2,l2,m2,n2,o2,p2,q2,r2,s2=KNN(X_train,y_train,X_test,y_test,a,l)
  print("\n........Loading.........")
  print("\n This might take some couple of minutes due to bulk nature of the algorithm")
  print("\n Kindly do bear")
  a3,b3,c3,d3,e3,f3,g3,h3,i3,j3,k3,l3,m3,n3,o3,p3,q3,r3,s3=svc_linear(X_train,y_train,X_test,y_test,a,l)
  a4,b4,c4,d4,e4,f4,g4,h4,i4,j4,k4,l4,m4,n4,o4,p4,q4,r4,s4=svc_poly(X_train,y_train,X_test,y_test,a,l)
  a5,b5,c5,d5,e5,f5,g5,h5,i5,j5,k5,l5,m5,n5,o5,p5,q5,r5,s5=svc_rbf(X_train,y_train,X_test,y_test,a,l)
  print("\n........Loading.........")
  a6,b6,c6,d6,e6,f6,g6,h6,i6,j6,k6,l6,m6,n6,o6,p6,q6,r6,s6=svc_sig(X_train,y_train,X_test,y_test,a,l)
  a7,b7,c7,d7,e7,f7,g7,h7,i7,j7,k7,l7,m7,n7,o7,p7,q7,r7,s7= Naives_cla(X_train,y_train,X_test,y_test,a,l)
  c,a8,b8,c8,d8,e8,f8,g8,h8,i8,j8,k8,l8,m8,n8,o8,p8,q8,r8,s8=DTC(X_train,y_train,X_test,y_test,a,l)
  t,c,a9,b9,c9,d9,e9,f9,g9,h9,i9,j9,k9,l9,m9,n9,o9,p9,q9,r9,s9=RFC(X_train,y_train,X_test,y_test,a,l)
  print("\nAccuracy results are in !.")
  print("\nGenerating Dataframe for the same..")
  for i in range(21):
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()
    sleep(0.25)
  print("\n Note: Incase if the Error , deviance values are high please use data preprocessing tools to scale down the value of the feature and try to run the algorithm again")
  data = {'Type of Classification':['Logistic Regression', 'K-Nearest-Neighbors', 'Support Vector Classifier (kernel="linear") a.k.a (Support Vector Machiene)','Support Vector Classifier(kernel="poly")','Support Vector Classifier(kernel="rbf")','Support Vector Classifier(kernel="sigmoid")','Naive Bayes Classification','Decision Tree Classification','Random Forest Classification'], 'Accuracy classification score':[a1,a2,a3,a4,a5,a6,a7,a8,a9],'Balanced Accuracy':[b1,b2,b3,b4,b5,b6,b7,b8,b9],'Cohen’s kappa Score':[c1,c2,c3,c4,c5,c6,c7,c8,c9],'F-measure(macro)':[d1,d2,d3,d4,d5,d6,d7,d8,d9],'F-measure(micro)':[e1,e2,e3,e4,e5,e6,e7,e8,e9],'F-measure(weighted)':[f1,f2,f3,f4,f5,f6,f7,f8,f9],'F-beta score(macro)':[g1,g2,g3,g4,g5,g6,g7,g8,g9],'F-beta score(micro)':[h1,h2,h3,h4,h5,h6,h7,h8,h9],'F-beta score(weighted)':[i1,i2,i3,i4,i5,i6,i7,i8,i9],'Average Hamming Loss':[j1,j2,j3,j4,j5,j6,j7,j8,j9],'Jaccards Score(macro)':[k1,k2,k3,k4,k5,k6,k7,k8,k9],'Matthews correlation coefficient (MCC)':[l1,l2,l3,l4,l5,l6,l7,l8,l9],'precision score(macro)':[m1,m2,m3,m4,m5,m6,m7,m8,m9],'precision-score(micro)':[n1,n2,n3,n4,n5,n6,n7,n8,n9],'precision-score(weighted)':[o1,o2,o3,o4,o5,o6,o7,o8,o9],'recall-score(macro)':[p1,p2,p3,p4,p5,p6,p7,p8,p9],'recall score(micro)':[q1,q2,q3,q4,q5,q6,q7,q8,q9],'recall score(weighted)':[r1,r2,r3,r4,r5,r6,r7,r8,r9],'Zero-one classification loss':[s1,s2,s3,s4,s5,s6,s7,s8,s9]} 
  df = pd.DataFrame(data) 
  display(df)
  while True:
    print("\n For further accuracy results like confusion matrix and so on do select a choice below")
    print("\n 1)Logistic Regression Results,2) KNN results,3)SVC Kernel='Linear'reults,4) SVC kernel='poly'results")
    print("\n5) SVC kernel='rbf'results,6)SVC kernel='sigmoid'results,7) Naive Bayes Classification Results results,8) Decision Tree Classification Results,9)Random Forest Classification Results")
    print("\n\t10) All the models results else exit")
    ch=int(input("Enter your preffered choice"))
    if ch==1:
      log_res(X_train,y_train,X_test,y_test,b,a)
    elif ch==2:
      KNN_res(X_train,y_train,X_test,y_test,n,j,s,b,a)
    elif ch==3:
      SVC_lin_res(X_train,y_train,X_test,y_test,b,a)
    elif ch==4:
      SVC_poly_res(X_train,y_train,X_test,y_test,b,a)
    elif ch==5:
      SVC_rbf_res(X_train,y_train,X_test,y_test,b,a)
    elif ch==6:
      SVC_sig_res(X_train,y_train,X_test,y_test,b,a)
    elif ch==7:
      Naives_res(X_train,y_train,X_test,y_test,b,a)
    elif ch==8:
      DTC_res(X_train,y_train,X_test,y_test,c,b,a)
    elif ch==9:
      RFC_res(X_train,y_train,X_test,y_test,t,c,b,a)
    elif ch==10:
      log_res(X_train,y_train,X_test,y_test,b,a)
      KNN_res(X_train,y_train,X_test,y_test,n,j,s,b,a)
      SVC_lin_res(X_train,y_train,X_test,y_test,b,a)
      SVC_poly_res(X_train,y_train,X_test,y_test,b,a)
      SVC_rbf_res(X_train,y_train,X_test,y_test,b,a)
      SVC_sig_res(X_train,y_train,X_test,y_test,b,a)
      DTC_res(X_train,y_train,X_test,y_test,c,b,a)
      RFC_res(X_train,y_train,X_test,y_test,t,c,b,a)
    else:
      break

def Naives_res(X_train,y_train,X_test,y_test,p,a):
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,log_loss,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  from sklearn.naive_bayes import GaussianNB
  classifier = GaussianNB()
  classifier.fit(X_train, y_train)
  y_pred=classifier.predict(X_test)
  print("\n NAIVE BAYES RESULTS:")
  print("\n Confusion Matrix")
  print("\n")
  print(confusion_matrix(y_test,y_pred))
  print("\n Precision score-max,micro,weighted")
  print("\n")
  f22=precision_recall_fscore_support(y_test, y_pred, average='macro')
  print(f22)
  print("\n")
  f23=precision_recall_fscore_support(y_test, y_pred, average='micro')
  print(f23)
  print("\n")
  f24=precision_recall_fscore_support(y_test, y_pred, average='weighted')
  print(f24)
  print("\n")

def Naives_cla(X_train,y_train,X_test,y_test,a,l):
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,log_loss,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  from sklearn.naive_bayes import GaussianNB
  classifier = GaussianNB()
  classifier.fit(X_train, y_train)
  y_pred=classifier.predict(X_test)
  f1=(abs(accuracy_score(y_test,y_pred))*100)
  f2=(abs(balanced_accuracy_score(y_test, y_pred))*100)
  f3=(abs(cohen_kappa_score(y_test,y_pred))*100)
  f4= f1_score(y_test, y_pred,average='macro')
  f5= f1_score(y_test, y_pred,average='micro')
  f6= f1_score(y_test, y_pred,average='weighted')
  f7=fbeta_score(y_test, y_pred, average='macro', beta=l)
  f8=fbeta_score(y_test, y_pred, average='micro', beta=l)
  f9=fbeta_score(y_test, y_pred, average='weighted',beta=l)
  f10=hamming_loss(y_test, y_pred)
  f11=jaccard_score(y_test, y_pred, average='macro')
  f12=matthews_corrcoef(y_test, y_pred)
  f13=precision_score(y_test, y_pred, average='macro')
  f14=precision_score(y_test, y_pred, average='micro')
  f15=precision_score(y_test, y_pred, average='weighted')
  f16=recall_score(y_test, y_pred, average='macro')
  f17=recall_score(y_test, y_pred, average='micro')
  f18=recall_score(y_test, y_pred, average='weighted')
  f19=zero_one_loss(y_test,y_pred)
  return f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19

def log_reg(X_train,y_train,X_test,y_test,a,l):
  from sklearn.linear_model import LogisticRegression
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,log_loss,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  regressor = LogisticRegression()
  regressor.fit(X_train, y_train)
  y_pred = regressor.predict(X_test)
  f1=(abs(accuracy_score(y_test,y_pred))*100)
  f2=(abs(balanced_accuracy_score(y_test, y_pred))*100)
  f3=(abs(cohen_kappa_score(y_test,y_pred))*100)
  f4= f1_score(y_test, y_pred,average='macro')
  f5= f1_score(y_test, y_pred,average='micro')
  f6= f1_score(y_test, y_pred,average='weighted')
  f7=fbeta_score(y_test, y_pred, average='macro', beta=l)
  f8=fbeta_score(y_test, y_pred, average='micro', beta=l)
  f9=fbeta_score(y_test, y_pred, average='weighted',beta=l)
  f10=hamming_loss(y_test, y_pred)
  f11=jaccard_score(y_test, y_pred, average='macro')
  f12=matthews_corrcoef(y_test, y_pred)
  f13=precision_score(y_test, y_pred, average='macro')
  f14=precision_score(y_test, y_pred, average='micro')
  f15=precision_score(y_test, y_pred, average='weighted')
  f16=recall_score(y_test, y_pred, average='macro')
  f17=recall_score(y_test, y_pred, average='micro')
  f18=recall_score(y_test, y_pred, average='weighted')
  f19=zero_one_loss(y_test,y_pred)
  return f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19

def log_res(X_train,y_train,X_test,y_test,p,a):
  from sklearn.linear_model import LogisticRegression
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  regressor = LogisticRegression()
  regressor.fit(X_train, y_train)
  y_pred = regressor.predict(X_test)
  print("\nLOGISTIC REGRESSION DETAILED REPORT:")
  print("\n Confusion Matrix")
  print("\n")
  print(confusion_matrix(y_test,y_pred))
  print("\n Precision score-max,micro,weighted")
  print("\n")
  f22=precision_recall_fscore_support(y_test, y_pred, average='macro')
  print(f22)
  print("\n")
  f23=precision_recall_fscore_support(y_test, y_pred, average='micro')
  print(f23)
  print("\n")
  f24=precision_recall_fscore_support(y_test, y_pred, average='weighted')
  print(f24)
  print("\n")

def KNN_res(X_train,y_train,X_test,y_test,n,j,s,P,a):
  from sklearn.neighbors import KNeighborsClassifier
  classifier = KNeighborsClassifier(n_neighbors = n,weights=j, metric = 'minkowski', p = s)
  classifier.fit(X_train, y_train)
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  classifier.fit(X_train, y_train)
  y_pred = classifier.predict(X_test)
  print("\n K-NEAREST NEIGHBORS DETAILED REPORT:")
  print("\n Confusion Matrix")
  print("\n")
  print(confusion_matrix(y_test,y_pred))
  print("\n Precision Score-macro,micro,weighted")
  print("\n")
  f22=precision_recall_fscore_support(y_test, y_pred, average='macro')
  print(f22)
  print("\n")
  f23=precision_recall_fscore_support(y_test, y_pred, average='micro')
  print(f23)
  print("\n")
  f24=precision_recall_fscore_support(y_test, y_pred, average='weighted')
  print(f24)
  print("\n")
  
def KNN(X_train,y_train,X_test,y_test,a,l):
  n=int(input("enter number of neighbors for KNN"))
  print("\n uniform,distance")
  j=input("enter type of weights from the above options for KNN")
  print("\n 1)Manhattan distance,2)euclidean_distance")
  s=int(input("Enter the preffered choice number from the above options for KNN"))
  from sklearn.neighbors import KNeighborsClassifier
  classifier = KNeighborsClassifier(n_neighbors = n,weights=j, metric = 'minkowski', p = s)
  classifier.fit(X_train, y_train)
  y_pred=classifier.predict(X_test)
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  f1=(abs(accuracy_score(y_test,y_pred))*100)
  f2=(abs(balanced_accuracy_score(y_test, y_pred))*100)
  f3=(abs(cohen_kappa_score(y_test,y_pred))*100)
  f4= f1_score(y_test, y_pred,average='macro')
  f5= f1_score(y_test, y_pred,average='micro')
  f6= f1_score(y_test, y_pred,average='weighted')
  f7=fbeta_score(y_test, y_pred, average='macro', beta=l)
  f8=fbeta_score(y_test, y_pred, average='micro', beta=l)
  f9=fbeta_score(y_test, y_pred, average='weighted',beta=l)
  f10=hamming_loss(y_test, y_pred)
  f11=jaccard_score(y_test, y_pred, average='macro')
  f12=matthews_corrcoef(y_test, y_pred)
  f13=precision_score(y_test, y_pred, average='macro')
  f14=precision_score(y_test, y_pred, average='micro')
  f15=precision_score(y_test, y_pred, average='weighted')
  f16=recall_score(y_test, y_pred, average='macro')
  f17=recall_score(y_test, y_pred, average='micro')
  f18=recall_score(y_test, y_pred, average='weighted')
  f19=zero_one_loss(y_test,y_pred)
  return n,j,s,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19

def SVC_lin_res(X_train,y_train,X_test,y_test,p,a):
  from sklearn.svm import SVC
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  classifier= SVC(kernel = 'linear',random_state=0)
  classifier.fit(X_train, y_train)
  y_pred = classifier.predict(X_test)
  print("\nSVC KERNEL-'LINEAR' DETAILED REPORT:")
  print("\n Confusion Matrix")
  print("\n")
  print(confusion_matrix(y_test,y_pred))
  print("\n Precision Score-macro,micro,weighted")
  print("\n")
  f22=precision_recall_fscore_support(y_test, y_pred, average='macro')
  print(f22)
  print("\n")
  f23=precision_recall_fscore_support(y_test, y_pred, average='micro')
  print(f23)
  print("\n")
  f24=precision_recall_fscore_support(y_test, y_pred, average='weighted')
  print(f24)
  print("\n")

def svc_linear(X_train,y_train,X_test,y_test,a,l):
  from sklearn.svm import SVC
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  classifier= SVC(kernel = 'linear',random_state=0)
  classifier.fit(X_train, y_train)
  y_pred = classifier.predict(X_test)
  f1=(abs(accuracy_score(y_test,y_pred))*100)
  f2=(abs(balanced_accuracy_score(y_test, y_pred))*100)
  f3=(abs(cohen_kappa_score(y_test,y_pred))*100)
  f4= f1_score(y_test, y_pred,average='macro')
  f5= f1_score(y_test, y_pred,average='micro')
  f6= f1_score(y_test, y_pred,average='weighted')
  f7=fbeta_score(y_test, y_pred, average='macro', beta=l)
  f8=fbeta_score(y_test, y_pred, average='micro', beta=l)
  f9=fbeta_score(y_test, y_pred, average='weighted',beta=l)
  f10=hamming_loss(y_test, y_pred)
  f11=jaccard_score(y_test, y_pred, average='macro')
  f12=matthews_corrcoef(y_test, y_pred)
  f13=precision_score(y_test, y_pred, average='macro')
  f14=precision_score(y_test, y_pred, average='micro')
  f15=precision_score(y_test, y_pred, average='weighted')
  f16=recall_score(y_test, y_pred, average='macro')
  f17=recall_score(y_test, y_pred, average='micro')
  f18=recall_score(y_test, y_pred, average='weighted')
  f19=zero_one_loss(y_test,y_pred)
  return f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19


def SVC_poly_res(X_train,y_train,X_test,y_test,p,a):
  from sklearn.svm import SVC
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  classifier= SVC(kernel = 'poly',random_state=0)
  classifier.fit(X_train, y_train)
  y_pred = classifier.predict(X_test)
  print("\nSVC KERNEL='POLY' DETAILED REPORT:")
  print("\n Confusion Matrix")
  print("\n")
  print(confusion_matrix(y_test,y_pred))
  print("\n Precision Score-macro,micro,weighted")
  print("\n")
  f22=precision_recall_fscore_support(y_test, y_pred, average='macro')
  print(f22)
  print("\n")
  f23=precision_recall_fscore_support(y_test, y_pred, average='micro')
  print(f23)
  print("\n")
  f24=precision_recall_fscore_support(y_test, y_pred, average='weighted')
  print(f24)
  print("\n")

def svc_poly(X_train,y_train,X_test,y_test,a,l):
  from sklearn.svm import SVC
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  classifier= SVC(kernel = 'poly',random_state=0)
  classifier.fit(X_train, y_train)
  y_pred = classifier.predict(X_test)
  f1=(abs(accuracy_score(y_test,y_pred))*100)
  f2=(abs(balanced_accuracy_score(y_test, y_pred))*100)
  f3=(abs(cohen_kappa_score(y_test,y_pred))*100)
  f4= f1_score(y_test, y_pred,average='macro')
  f5= f1_score(y_test, y_pred,average='micro')
  f6= f1_score(y_test, y_pred,average='weighted')
  f7=fbeta_score(y_test, y_pred, average='macro', beta=l)
  f8=fbeta_score(y_test, y_pred, average='micro', beta=l)
  f9=fbeta_score(y_test, y_pred, average='weighted',beta=l)
  f10=hamming_loss(y_test, y_pred)
  f11=jaccard_score(y_test, y_pred, average='macro')
  f12=matthews_corrcoef(y_test, y_pred)
  f13=precision_score(y_test, y_pred, average='macro')
  f14=precision_score(y_test, y_pred, average='micro')
  f15=precision_score(y_test, y_pred, average='weighted')
  f16=recall_score(y_test, y_pred, average='macro')
  f17=recall_score(y_test, y_pred, average='micro')
  f18=recall_score(y_test, y_pred, average='weighted')
  f19=zero_one_loss(y_test,y_pred)
  return f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19

  
def SVC_rbf_res(X_train,y_train,X_test,y_test,p,a):
  from sklearn.svm import SVC
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  classifier= SVC(kernel = 'rbf',random_state=0)
  classifier.fit(X_train, y_train)
  y_pred = classifier.predict(X_test)
  print("\nSVC KERNEL='RBF' DETAILED REPORT:")
  print("\n Confusion Matrix")
  print("\n")
  print(confusion_matrix(y_test,y_pred))
  print("\n Precision Score-macro,micro,weighted")
  print("\n")
  f22=precision_recall_fscore_support(y_test, y_pred, average='macro')
  print(f22)
  print("\n")
  f23=precision_recall_fscore_support(y_test, y_pred, average='micro')
  print(f23)
  print("\n")
  f24=precision_recall_fscore_support(y_test, y_pred, average='weighted')
  print(f24)
  print("\n")

def svc_rbf(X_train,y_train,X_test,y_test,a,l):
  from sklearn.svm import SVC
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  classifier= SVC(kernel = 'rbf',random_state=0)
  classifier.fit(X_train, y_train)
  y_pred = classifier.predict(X_test)
  f1=(abs(accuracy_score(y_test,y_pred))*100)
  f2=(abs(balanced_accuracy_score(y_test, y_pred))*100)
  f3=(abs(cohen_kappa_score(y_test,y_pred))*100)
  f4= f1_score(y_test, y_pred,average='macro')
  f5= f1_score(y_test, y_pred,average='micro')
  f6= f1_score(y_test, y_pred,average='weighted')
  f7=fbeta_score(y_test, y_pred, average='macro', beta=l)
  f8=fbeta_score(y_test, y_pred, average='micro', beta=l)
  f9=fbeta_score(y_test, y_pred, average='weighted',beta=l)
  f10=hamming_loss(y_test, y_pred)
  f11=jaccard_score(y_test, y_pred, average='macro')
  f12=matthews_corrcoef(y_test, y_pred)
  f13=precision_score(y_test, y_pred, average='macro')
  f14=precision_score(y_test, y_pred, average='micro')
  f15=precision_score(y_test, y_pred, average='weighted')
  f16=recall_score(y_test, y_pred, average='macro')
  f17=recall_score(y_test, y_pred, average='micro')
  f18=recall_score(y_test, y_pred, average='weighted')
  f19=zero_one_loss(y_test,y_pred)
  return f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19

  
def SVC_sig_res(X_train,y_train,X_test,y_test,p,a):
  from sklearn.svm import SVC
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  classifier= SVC(kernel = 'sigmoid',random_state=0)
  classifier.fit(X_train, y_train)
  y_pred = classifier.predict(X_test)
  print("\nSVC KERNEL='SIGMOID' FURTHER RESULTS:")
  print("\n Confusion Matrix")
  print("\n")
  print(confusion_matrix(y_test,y_pred))
  print("\n Precision Score-macro,micro,weighted")
  print("\n")
  f22=precision_recall_fscore_support(y_test, y_pred, average='macro')
  print(f22)
  print("\n")
  f23=precision_recall_fscore_support(y_test, y_pred, average='micro')
  print(f23)
  print("\n")
  f24=precision_recall_fscore_support(y_test, y_pred, average='weighted')
  print(f24)
  print("\n")

def svc_sig(X_train,y_train,X_test,y_test,a,l):
  from sklearn import metrics
  from sklearn.svm import SVC
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  classifier= SVC(kernel = 'sigmoid',random_state=0)
  classifier.fit(X_train, y_train)
  y_pred = classifier.predict(X_test)
  f1=(abs(accuracy_score(y_test,y_pred))*100)
  f2=(abs(balanced_accuracy_score(y_test, y_pred))*100)
  f3=(abs(cohen_kappa_score(y_test,y_pred))*100)
  f4= f1_score(y_test, y_pred,average='macro')
  f5= f1_score(y_test, y_pred,average='micro')
  f6= f1_score(y_test, y_pred,average='weighted')
  f7=fbeta_score(y_test, y_pred, average='macro', beta=l)
  f8=fbeta_score(y_test, y_pred, average='micro', beta=l)
  f9=fbeta_score(y_test, y_pred, average='weighted',beta=l)
  f10=hamming_loss(y_test, y_pred)
  f11=jaccard_score(y_test, y_pred, average='macro')
  f12=matthews_corrcoef(y_test, y_pred)
  f13=precision_score(y_test, y_pred, average='macro')
  f14=precision_score(y_test, y_pred, average='micro')
  f15=precision_score(y_test, y_pred, average='weighted')
  f16=recall_score(y_test, y_pred, average='macro')
  f17=recall_score(y_test, y_pred, average='micro')
  f18=recall_score(y_test, y_pred, average='weighted')
  f19=zero_one_loss(y_test,y_pred)
  return f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19


def DTC_res(X_train,y_train,X_test,y_test,c,p,a):
  from sklearn.tree import DecisionTreeClassifier
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  classifier= DecisionTreeClassifier(criterion= c,random_state=0)
  classifier.fit(X_train, y_train)
  y_pred = classifier.predict(X_test)
  print("\n DECISION TREE CLASSIFICATION DETAILED REPORT:")
  print("\n Confusion Matrix")
  print("\n")
  print(confusion_matrix(y_test,y_pred))
  print("\n Precision Score-macro,micro,weighted")
  print("\n")
  f22=precision_recall_fscore_support(y_test, y_pred, average='macro')
  print(f22)
  print("\n")
  f23=precision_recall_fscore_support(y_test, y_pred, average='micro')
  print(f23)
  print("\n")
  f24=precision_recall_fscore_support(y_test, y_pred, average='weighted')
  print(f24)
  print("\n")

def DTC(X_train,y_train,X_test,y_test,a,l):
  print("\n gini,entropy")
  c=input("enter type of criteria from the above choice for decision tree classification ")
  from sklearn.tree import DecisionTreeClassifier
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  classifier= DecisionTreeClassifier(criterion= c,random_state=0)
  classifier.fit(X_train, y_train)
  y_pred = classifier.predict(X_test)
  f1=(abs(accuracy_score(y_test,y_pred))*100)
  f2=(abs(balanced_accuracy_score(y_test, y_pred))*100)
  f3=(abs(cohen_kappa_score(y_test,y_pred))*100)
  f4= f1_score(y_test, y_pred,average='macro')
  f5= f1_score(y_test, y_pred,average='micro')
  f6= f1_score(y_test, y_pred,average='weighted')
  f7=fbeta_score(y_test, y_pred, average='macro', beta=l)
  f8=fbeta_score(y_test, y_pred, average='micro', beta=l)
  f9=fbeta_score(y_test, y_pred, average='weighted',beta=l)
  f10=hamming_loss(y_test, y_pred)
  f11=jaccard_score(y_test, y_pred, average='macro')
  f12=matthews_corrcoef(y_test, y_pred)
  f13=precision_score(y_test, y_pred, average='macro')
  f14=precision_score(y_test, y_pred, average='micro')
  f15=precision_score(y_test, y_pred, average='weighted')
  f16=recall_score(y_test, y_pred, average='macro')
  f17=recall_score(y_test, y_pred, average='micro')
  f18=recall_score(y_test, y_pred, average='weighted')
  f19=zero_one_loss(y_test,y_pred)
  return c,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19


def RFC_res(X_train,y_train,X_test,y_test,t,c,p,a):
  from sklearn.ensemble import RandomForestClassifier
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  classifier= RandomForestClassifier(n_estimators = t,criterion=c, random_state = 0)
  classifier.fit(X_train, y_train)
  y_pred = classifier.predict(X_test)
  print("\n RANDOM FOREST CLASSIFICATION - DETAILED REPORT:")
  print("\n Confusion Matrix")
  print("\n")
  print(confusion_matrix(y_test,y_pred))
  print("\n Precision Score-macro,micro,weighted")
  print("\n")
  f22=precision_recall_fscore_support(y_test, y_pred, average='macro')
  print(f22)
  print("\n")
  f23=precision_recall_fscore_support(y_test, y_pred, average='micro')
  print(f23)
  print("\n")
  f24=precision_recall_fscore_support(y_test, y_pred, average='weighted')
  print(f24)
  print("\n")

def RFC(X_train,y_train,X_test,y_test,a,l):
  from sklearn.ensemble import RandomForestClassifier
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  t=int(input("Enter number of trees for Random Forest Classification"))
  print("\n gini,entropy")
  c=input("enter type of criteria from the above choice for Random Forest Classification")
  classifier= RandomForestClassifier(n_estimators = t,criterion=c, random_state = 0)
  classifier.fit(X_train, y_train)
  y_pred = classifier.predict(X_test)
  f1=(abs(accuracy_score(y_test,y_pred))*100)
  f2=(abs(balanced_accuracy_score(y_test, y_pred))*100)
  f3=(abs(cohen_kappa_score(y_test,y_pred))*100)
  f4= f1_score(y_test, y_pred,average='macro')
  f5= f1_score(y_test, y_pred,average='micro')
  f6= f1_score(y_test, y_pred,average='weighted')
  f7=fbeta_score(y_test, y_pred, average='macro', beta=l)
  f8=fbeta_score(y_test, y_pred, average='micro', beta=l)
  f9=fbeta_score(y_test, y_pred, average='weighted',beta=l)
  f10=hamming_loss(y_test, y_pred)
  f11=jaccard_score(y_test, y_pred, average='macro')
  f12=matthews_corrcoef(y_test, y_pred)
  f13=precision_score(y_test, y_pred, average='macro')
  f14=precision_score(y_test, y_pred, average='micro')
  f15=precision_score(y_test, y_pred, average='weighted')
  f16=recall_score(y_test, y_pred, average='macro')
  f17=recall_score(y_test, y_pred, average='micro')
  f18=recall_score(y_test, y_pred, average='weighted')
  f19=zero_one_loss(y_test,y_pred)
  return t,c,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19
