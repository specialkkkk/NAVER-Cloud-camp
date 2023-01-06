import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split


#1. 데이터
x = np.array(range(1, 17))          # 1~ 16
y = np.array(range(1, 17))




x_train, x_test, y_train, y_test = train_test_split(
    x,y,
    train_size=0.8,
    test_size=0.2,
    random_state=123
)


print(x_train.shape, x_test.shape) # (12,) (4,)
print(y_train.shape, y_test.shape) # (12,) (4,)





#2. 모델구성
model = Sequential()
model.add(Dense(5, input_dim=1))
model.add(Dense(3, activation='relu'))
model.add(Dense(1))

#3. 컴파일, 훈련
model.compile(loss='mse', optimizer='adam')
model.fit(x_train, y_train, epochs=100, batch_size=1,
          validation_split=0.25)



#4. 평가,예측
loss = model.evaluate(x_test, y_test)
print('loss : ', loss)

result = model.predict([17])
print("17의 예측값 : ", result)

