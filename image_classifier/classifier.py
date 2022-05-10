# %%
import tensorflow as tf, numpy as np, time
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import TensorBoard

# %%
import pickle
x = pickle.load(open('D:\machine_learning\image_classification\chapadao\X_chapadao.pickle','rb'))
x = x/255.0
y = np.array(pickle.load(open('D:\machine_learning\image_classification\chapadao\Y_chapadao.pickle','rb')))

# %%
# melhor resultado: (6,1,32)
conv_layers = [6] #[2]#[1,2,3]
dense_layers = [3] #[3] #[0,1,2]
layer_sizes = [32] #[64] #[32,64,128]

# %%
for conv_layer in conv_layers:
    for dense_layer in dense_layers:
        for layer_size in layer_sizes:
            # cl=convolutional layers, dl=dense layers, ls=layer size, bs=batch size
            name = f'{conv_layer}_cl_{dense_layer}_dl_{layer_size}_ls_5_bs'
            name = 'juba'
            tensorboard = TensorBoard(log_dir=f'D:\machine_learning\image_classification\chapadao\logs\{name}',update_freq='epoch')
            
            model = Sequential()
            
            model.add(Conv2D(layer_size, (3,3), input_shape=x.shape[1:]))
            model.add(Activation('relu'))
            model.add(MaxPooling2D(pool_size=(2,2)))

            for cl in range(conv_layer-1):
                model.add(Conv2D(layer_size, (3,3)))
                model.add(Activation('relu'))
                model.add(MaxPooling2D(pool_size=(2,2)))

            model.add(Flatten())
            for dl in range(dense_layer):
                model.add(Dense(layer_size))
                model.add(Activation('relu'))

            model.add(Dense(1))
            model.add(Activation('sigmoid'))

            model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])

            model.fit(x,y,validation_split=0.2, epochs=15, batch_size=5, callbacks=[tensorboard])
            
            print(dir(model))

# %%



