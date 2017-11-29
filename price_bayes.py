import os
import itertools
import numpy as np
import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import GaussianNB
import math
import sys
from time import time




COLUMNS = ["open",
                "close",
                "high",
                "low",
                "volume",
                "median_prior",
                "stdv_prior",
                "deep_median",
                "deep_stdv",
                "growth",
                "difference",
                "buy",
                "sell",

]
    
def convertToNumber (s):
    return int.from_bytes(s.encode(), 'big')   

def float_array(string_array):
  
  a_i = 0
  while a_i < len(string_array):
      string_array[a_i] = convertToNumber(string_array[a_i])
      a_i+=1
  
  re_string_array=string_array.astype(np.float64)
  re_string_array=normalize_column(re_string_array)
  return re_string_array



def normalize_column(col):
    return (col-min(col))/(max(col)-min(col))





def make_input_fn(filename,split=0,full=0):
  """Input builder function."""
  df = pd.read_csv(filename,
  names=COLUMNS,
  skipinitialspace=True,
  converters={  'open': np.float64,
                'close': np.float64,
                'high': np.float64,
                'low': np.float64,
                'volume': np.float64,
                'median_prior': np.float64,
                'stdv_prior': np.float64,
                'deep_median': np.float64,
                'deep_stdv': np.float64,
                'growth': np.float64,
                'difference': np.float64,
                'buy': np.float64,
                'sell': np.float64},
  engine="python", 
  skiprows=1)
  labels = df['buy']
  #normalize the numeric columns

  df["open"] = normalize_column(df["open"].values)
  df["close"] = (df["close"].values)
  df["high"] = normalize_column(df["high"].values)
  df["low"] = normalize_column(df["low"].values)
  df["volume"] = normalize_column(df["volume"].values)
  df["median_prior"] = normalize_column(df["median_prior"].values)
  df["stdv_prior"] = normalize_column(df["stdv_prior"].values)
  df["deep_median"] = normalize_column(df["deep_median"].values)
  df["deep_stdv"] = normalize_column(df["deep_stdv"].values)
  df["growth"] = normalize_column(df["growth"].values)
  df["difference"] = normalize_column(df["difference"].values)
  

  train_features = [
                         
              np.array(df["open"].values, dtype=np.float64),
              np.array(df["close"].values, dtype=np.float64),
              np.array(df["high"].values, dtype=np.float64),
              np.array(df["low"].values, dtype=np.float64),
              np.array(df["volume"].values, dtype=np.float64), 
              np.array(df["median_prior"].values, dtype=np.float64),
              np.array(df["stdv_prior"].values, dtype=np.float64),
              np.array(df["deep_median"].values, dtype=np.float64),
              np.array(df["deep_stdv"].values, dtype=np.float64),
              np.array(df["growth"].values, dtype=np.float64),
              np.array(df["difference"].values, dtype=np.float64),
              #np.array(df["part_nbr"].values, dtype=np.str),                         
   ]
  
  x = np.array(df["buy"].values, dtype=np.float64)
  x_i = 0
  while x_i < (len(x)):
      if(x[x_i]==0):
          x[x_i] = 0
      else:
          x[x_i] = 1
      x_i +=1
  x=x.astype(np.float64)

  
  y = np.array(df["sell"].values, dtype=np.float64)
  x_i = 0
  while x_i < (len(x)):
      if(y[x_i]==1):
          x[x_i] = 2
      x_i +=1
  x=x.astype(np.float64)
  test_lbl = x
  
  
  flat_test_list = []
  #Features are stored as features[][]
  outer_count = 0
  inner_count = 0
  deep_inner_count = 0
  a = labels
  size_of_input = len(a)
  
  """
  if(full ==1):
      while(outer_count < len(train_features[0])):
          while(inner_count < len(train_features)):
              #appends a feature to the list, and then appends 28 other features to that list
              while(deep_inner_count < len(train_features)):
              #We want to map each feature to every other feature in our list
                 if(deep_inner_count != inner_count):
                     flat_test_list.append(train_features[deep_inner_count][inner_count])
                 deep_inner_count +=1
              inner_count+=1
              deep_inner_count = 0
          outer_count+=1
          inner_count = 0
       
    
          
      print(len(flat_test_list))                           
      test_features = np.reshape(flat_test_list, (812,size_of_input)).T
      test_labels = np.reshape(test_lbl, ((size_of_input))).T
  """    
  if(full == 0):
      while(outer_count < len(train_features)):
          while(inner_count < len(train_features[0])):
              flat_test_list.append(train_features[outer_count][inner_count])
              inner_count+=1
          outer_count+=1
          inner_count = 0
     
      test_features = np.reshape(flat_test_list, (11,size_of_input)).T
      test_labels = np.reshape(test_lbl, ((size_of_input))).T

  
  if(split == 1):        
    x_train, x_test, y_train, y_test = train_test_split(
      test_features, test_labels, test_size=0.3, random_state=42)  
    return  x_train, x_test, y_train, y_test


  if(split == 0):
      val = len(test_labels)
      qi = 0
      temp_train_features = np.empty(0)
      temp_train_labels = np.empty(0)
      temp_test_features = np.empty(0)
      temp_test_labels = np.empty(0)
      while qi < 800:
          temp_train_features = np.append(temp_train_features,test_features[qi])
          temp_train_labels = np.append(temp_train_labels, test_labels[qi])
          qi +=1
      while qi < val:
          temp_test_features = np.append(temp_test_features, test_features[qi])
          temp_test_labels = np.append(temp_test_labels, test_labels[qi])
          qi +=1
          
      temp_train_features = test_features
      temp_train_labels = test_labels
      temp_test_features = temp_test_features.reshape((val-800),11)
      temp_test_labels = temp_test_labels.reshape((val-800))
      
      return temp_train_features, temp_test_features, temp_train_labels, temp_test_labels
  
      
      
def bayes_runner():
    #train_features, test_features, train_labels, test_labels = make_input_fn_with_test_splitting("combinedstatus.csv")
    #test_features, test_labels = make_input_fn("rejectstatus.csv")
    train_features, test_features, train_labels, test_labels = make_input_fn("bit_DATA.csv", split = 0) 

    #test_features2, test_labels2 = make_input_fn("accpaidstatus.csv")      
    
    #We cant use normalized data
    #when the data is normalized each feature is dictated by other elements in the dataset, this makes prediction very difficult.
    #is the reason for horrible skewing in some cases.
    
    

    
    #print("Giving the model all rejects score: " + str(clg.score(test_features1, test_labels1)) )
    #print("Giving the model all Accepts score: " + str(clg.score(test_features1, test_labels1)) )
    
    
    
    action_list = []
    price_list = []
    
    
    clf = GaussianNB()
    clf.fit(train_features, train_labels)
    q = 0
    while(q < len(test_features)):
        temp = test_features[q][1].astype(np.float64)
        temp_deep = test_features[q][7].astype(np.float64)
        x = round(temp,2)
        y = round(temp_deep,2)
        #print("Action when price is " + str(x) + " And prior median is " + str(y) )
        z = clf.predict([test_features[q]])
        temp_real = test_labels
        real_lbls = np.asarray(temp_real)
        real = real_lbls[q]
        action_list.append(z)
        price_list.append(temp)
        """
        if(z == 0):
            print("Model chose HOLD")
        if(z == 1):
            print("Model chose BUY")
        if(z == 2):
            print("Model chose SELL")
        if(real == 0):
            print("HOLD was optimal")
        if(real == 1):
            print("BUY was optimal")
        if(real == 2):
            print("SELL was optimal")
        print("--------------------------------------------------------")
        """    
        q+=1
    print("Testing Model Score Gaussian: " + str(clf.score(test_features, test_labels)) )
    print("Converting into currency")
    invested_value = 100
    placement = 0
    act = 0
    while placement < len(action_list):
        #if we buy divide investment by cost of currency
        if (action_list[placement] == 1 and act!=1):
            invested_value = invested_value/price_list[placement]
            act = 1
            print("Purchased at interval " +str(placement+800) +" " + str(invested_value) + " shares")
        #if we sell multiply currency by its value
        elif(action_list[placement] == 2 and act==1):
            invested_value = invested_value * price_list[placement]
            act = 2
            print("sold at interval " +str(placement+800) +" $" + str(invested_value))
        placement+=1
    if(act == 1):
        invested_value = invested_value * price_list[(len(price_list))-1]
    print("You invested $100 its value is now $" + str(invested_value))
   
        
            
            
    
    
    
    
    #clf.fit(train_features, train_labels)
    #print("Training score using Gaussian Bayes: " + str(clf.score(train_features, train_labels)) )
    #print("Giving the model all accepts score: " + str(clf.score(test_features, test_labels)) )
    #print("Giving the model all rejects score: " + str(clf.score(test2_features, test2_labels)) )



    
   

bayes_runner()
