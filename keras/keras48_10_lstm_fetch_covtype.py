import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Conv2D, Flatten, LSTM
from sklearn.model_selection import train_test_split
from sklearn.datasets import fetch_covtype

#1. 데이터
datasets = fetch_covtype()
x = datasets.data
y = datasets.target
print(x.shape, y.shape)  # (581012, 54) (581012,)    #데이터 58만개  / 컬럼 54개 = input
print(np.unique(y, return_counts=True))  #(array([1, 2, 3, 4, 5, 6, 7]), array([211840, 283301,  35754,   2747,   9493,  17367,  20510], dtype=int64)) output= 7


from tensorflow.keras.utils import to_categorical
y = to_categorical(y)
print(y)
y = np.delete(y, 0 , axis = 1)
print(y.shape)   # y= 7


x_train, x_test, y_train, y_test = train_test_split(x, y, shuffle=True, random_state=333, test_size=0.2) #stratify=y 제거
print(y_train)
print(y_test)


######################################## 케라스 투카테고리컬##############################
# from tensorflow.kears.utils import to_categorical
# y = to_categorical(y)
# print(y.shape)   #  (581012, 8)
#print(type(y))      <class 'numpy.ndarray'>
#print(y[:10])
#print(np.unique(y[:,0]), return_counts=True))            [0.]
#print(np.unique(y[:,1]), return_counts=True))            [0, 1.]
#y = np.delete(y, 0, axis=1)
# print(shape.y) 
# print(y[:10])
#print(np.unique(y[:,0]), return_counts=True)
#평가,예측~
#########################################################################################

######################################## 판다스 겟더미스 #################################
# import pandas as pd
# y = pd.get_dummies(y)
# print(type(y[:10])
# print(type(y))   # <class 'pandas.core.frame.Data

# y = y.values     #  = 판다스 데이터 y가 넘파이로 바뀐다(넘파이로 바꿔야 인식됨)
# y = y.to_numpy   #  = 판다스 데이터 y가 넘파이로 바뀐다(넘파이로 바꿔야 인식됨)

# print(type(y))   # <class 'numpy.ndarray'>
# print(y.shape)   #   (581012, 7)

#########################################################################################

######################################### 사이킷런 전처리 ###################################
#  ★ 원핫인코더쓰고 toaraay로 바꿔준다. ★


# print(y.shape) (581012,)
# y = y.reshape(581012, 1)
# print(y.shape) (581012, 1)             
# from sklearn.preprocessing import OneHotEncoder
# ohe = OneHotEncoder()
# y = ohe.fit(y)                         
# y = ohe.transform(y)        두줄을 한줄로 쓰기  # y = ohe.fit_transform
# y = y.toarray()


# print(y[:15])
# print(type(y))  # <class 'scipy.sparse._csr.csr_matrix'>
# print(y.shape)  # (581012, 7)

#############################################################################################






from sklearn.preprocessing import MinMaxScaler, StandardScaler
scaler = MinMaxScaler()
# scaler = StandardScaler()

scaler.fit(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)




print(x_train.shape, x_test.shape) #(464809, 54) (116203, 54)



x_train = x_train.reshape(464809, 9, 6)
x_test = x_test.reshape(116203, 9, 6)
print(x_train.shape, x_test.shape)  #(464809, 54) (116203, 54)





#2. 모델 구성
model = Sequential()
model.add(LSTM(units=5, input_shape=(9,6)))
model.add(Dense(50, activation='relu'))
model.add(Dense(60, activation='relu'))
model.add(Dense(70, activation='relu'))
model.add(Dense(80, activation='relu'))
model.add(Dense(70, activation='relu'))
model.add(Dense(7, activation='softmax'))     #아웃풋= Y값

#3. 컴파일, 훈련
model.compile(loss='categorical_crossentropy', optimizer='adam',
              metrics=['accuracy'])
from tensorflow.keras.callbacks import EarlyStopping
earlyStopping = EarlyStopping(monitor='val_loss' , 
                              mode='min', 
                              patience=20, restore_best_weights=True,
                              verbose=1)
model.fit(x_train, y_train, epochs=100, batch_size=250,
          validation_split=0.2,
          callbacks=[earlyStopping],
          verbose=1)

#4. 평가,예측
loss, accuracy = model.evaluate(x_test, y_test)
print('loss : ', loss)
print('accuracy : ', accuracy)




from sklearn.metrics import accuracy_score
import numpy as np
y_predict = model.predict(x_test)
y_predict = np.argmax(y_predict, axis=1)
print("y_pred(예측값) : ", y_predict)
y_test = np.argmax(y_test, axis=1)
print("y_test(원래값) : ", y_test)

acc = accuracy_score(y_test, y_predict)   
print(acc)




# accuracy :  0.860287606716156
# accuracy :  0.9325060248374939  레이어 2의 배수 역삼각형

#-----------------CNN ------------------
# loss :  0.584589421749115
#accuracy :  0.7505744099617004