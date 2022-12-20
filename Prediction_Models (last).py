#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#초기 설정

pip install -U scikit-learn


# In[1]:


import modi
import numpy as np
import pandas as pd
import joblib
import time

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn import linear_model
from sklearn import metrics


# In[42]:


bundle = modi.MODI()


# In[2]:


#모델 학습하는 코드. 실제 학습한 모델은 pkl 파일로 저장해서 같이 보냈어요.

dataset = pd.read_csv('data.csv')

x_data = dataset[['AX', 'AY', 'AZ']]
labels = dataset['ActivityName']

X_train , X_test, y_train, y_test = train_test_split(x_data, labels, test_size=0.2, random_state=20)


def train_model(model, X_train, y_train, X_test, y_test):
    # to store results at various phases
    results = dict()
    model.fit(X_train, y_train)
    joblib.dump(model, 'save_model.pkl')
    print("done")

    
parameters = {'C':[0.01, 0.1, 1, 10, 20, 30], 'penalty':['l2']}
log_reg = linear_model.LogisticRegression()
log_reg_grid = GridSearchCV(log_reg, param_grid=parameters, cv=3, verbose=1, n_jobs=-1)

log_reg_grid_results =  train_model(log_reg_grid, X_train, y_train, X_test, y_test)


# In[3]:


"""
저장한 pkl 파일 불러와서 예측하는 모델.
저희 실제로 작성하는 코드에는 이 부분하고 아래 실행 코드만 넣어서 value 값으로 L / R
인식하시면 될 것 같아요!
"""
def predict_model(real_data):
    model_load = joblib.load('save_model.pkl') 
    value = model_load.predict(real_data)
    print(value)
    return value


# In[4]:


"""
실제 실행 시.
자이로 센서 받아서 인식하는 건 이미 지난주에 성공했었고, 저한테 센서가 없어서 제가 테스트 해볼 때는
그냥 제가 갖고 있던 왼쪽 데이터 파일 넣어서 실행해봤어요.
"""

while True:
    time.sleep(2)
    gyro = bundle.gyros[0]
    realX = gyro.acceleration_x
    realY = gyro.acceleration_y
    realZ = gyro.acceleration_z
    real_data_dict = {
        "AX" : [realX],
        "AY" : [realY],
        "AZ" : [realZ]
    }
    real_data = pd.DataFrame(data=real_data_dict)    
    predict_model(real_data)

