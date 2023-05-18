# %%
import os
from tensorflow.keras.utils import text_dataset_from_directory
import codecs
import tempfile
import json
import pandas as pd
import numpy as np

from keras.layers import Input, Dense, Activation, TimeDistributed, Softmax, TextVectorization, Reshape, RepeatVector, Conv1D, Bidirectional, AveragePooling1D, UpSampling1D, Embedding, Concatenate, GlobalAveragePooling1D, LSTM, Multiply, MultiHeadAttention
from keras.models import Model
import tensorflow as tf
from tensorflow import keras
import keras

from keras.layers import Input, TextVectorization
from keras.models import Model

from tensorflow.keras.callbacks import EarlyStopping

# %%
# DATASET_DIR = r'./WebscrapData/'
# vocab_size = 2500
# seq_len = 8

# %%
def get_data_gen(DATASET_DIR, vocab_size,seq_len):
    # Create an empty list to store the content data
    content_list = []

    # Iterate over the folders in the root directory
    for folder_name in os.listdir(DATASET_DIR):
        folder_path = os.path.join(DATASET_DIR, folder_name)
        
        # Check if the item in the root directory is a folder
        if os.path.isdir(folder_path):
            # Iterate over the JSON files in the folder
            for filename in os.listdir(folder_path):
                if filename.endswith('.json'):
                    file_path = os.path.join(folder_path, filename)
                    
                    # Read the JSON file
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                    
                    # Access the content component or any other data within the JSON
                    content = data['content']  # Replace 'content' with the actual key in your JSON
                    
                    # Append the content to the list
                    content_list.append(content)

    # Create a DataFrame from the content list
    df = pd.DataFrame({'content': content_list})

    dataset = tf.data.Dataset.from_tensor_slices(df['content'].values)
    
    # Batch the dataset
    batch_size = 16
    dataset = dataset.batch(batch_size)
    vectorize_layer = TextVectorization(max_tokens=vocab_size, output_sequence_length=seq_len)
    vectorize_layer.adapt(dataset)

    return vectorize_layer, dataset
        

# %%
# vectorize_layer, dataset = get_data_gen(DATASET_DIR, vocab_size,seq_len)

# %%
def rnn_model(seq_len, latent_dim, vocab_size):

    # define imput layer
    input_layer = Input(shape=(seq_len-1,))
    x = input_layer

    # add embedding layer
    x = Embedding(vocab_size, latent_dim, name='embedding', mask_zero=True)(x)

    # apply attention
    x = MultiHeadAttention(num_heads=3, key_dim=2)(x, value=x)

    # apply bidirectional LSTM
    x1 = LSTM(128)(x) #mexer nesse param
    x2 = LSTM(128, go_backwards=True)(x)

    # concatenate LSTM outputs
    x = Concatenate()([x1, x2])
    latent_rep = x

    # add final dense and softmax layers
    x = Dense(vocab_size)(x)
    x = Softmax()(x)

    # create and return model
    return Model(input_layer, x)

# %%
# model = rnn_model(seq_len, 512, vocab_size)

# %%
def create_and_train_model(model, vectorize_layer,dataset):
    # create predictor and latent model
    predictor = model

    # print model summary
    predictor.summary()

    # configure optimizer and loss function
    #opt = keras.optimizers.SGD(learning_rate=1, momentum=0.9)
    opt = keras.optimizers.Nadam(learning_rate=0.04)
    loss_fn = keras.losses.SparseCategoricalCrossentropy(
        ignore_class=1,
        name="sparse_categorical_crossentropy",
    )

    #compile the model
    predictor.compile(loss=loss_fn, optimizer=opt, metrics=["accuracy"])

    def separar_ultimo_token(x):
        x_ = vectorize_layer(x)
        x_ = x_[:,:-1]
        y_ = x_[:,-1:]
        return x_, y_
    
    dataset.map(separar_ultimo_token)

    early_stopping = EarlyStopping(patience=10, restore_best_weights=True, monitor='loss')
    history = predictor.fit(dataset.map(separar_ultimo_token), epochs=60, verbose=1, callbacks=[early_stopping])

    predictor.save('generativemodel.h5')

    return predictor

# %%
# predictor = create_and_train_model(model, vectorize_layer,dataset)

# %%
def predizer(entrada, numero_de_predicoes, modelo, vectorize_layer, temperature=0):
    frase = entrada.capitalize()
    contexto = frase # Contexto deslizante
    temperature = temperature

    for n in range(numero_de_predicoes):
        pred = modelo.predict(vectorize_layer([contexto])[:,:-1])

        # Nao repetir palavras
        tentando = True
        while tentando:

            # Selectionar de k-best
            candidatos = tf.math.top_k(pred, k=10).indices[0,:]
            idx = np.random.choice(candidatos.numpy())
            # idx = tf.argmax(pred, axis=1)[0]
            word = vectorize_layer.get_vocabulary()[idx]
            if word in frase.split():
                pred[0][idx] = 0
            else:
                tentando = False
                
        frase = frase + " " + word 
        contexto = contexto + " " + word
        #print(frase)
        contexto = ' '.join(frase.split()[1:])
        frase_final = frase + '.'
    return frase_final

# %%
# message = 'space'
# generated_text = predizer(message, 40, predictor, vectorize_layer, temperature=0)
# generated_text

# %%



