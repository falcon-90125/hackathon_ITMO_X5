import tensorflow as tf
import keras as keras
import numpy as np
import pandas as pd
import pickle #для сохранения и загрузки tokenizer'а

from keras import utils #утилита для работы с нейронными сетями
from keras.preprocessing.text import Tokenizer #для преобразования текстовых данных в числовые тензоры

from keras.models import Sequential # для создания архитектур нейронных сетей
from keras.models import load_model # для загрузки архитектур и весов нейронных сетей

# Загружаем файл с отзывами
shop_reviews = pd.read_excel('input/shop_reviews.xlsx')

def prediction_list(shop_reviews):

    # Загружаем файл tokenizer'а
    with open('input/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    maxWordsCount = 25000 # Размер словаря tokenizer'а

    # Преобразуем верификационную выборку в BOW
    shop_reviews_text = shop_reviews.text.tolist()
    testFinWordIndexes = tokenizer.texts_to_sequences(shop_reviews_text) # Тексты в индексы

    test = np.empty((0, maxWordsCount)) # Заготовка под верификационную выборку
    for i in range(len(testFinWordIndexes)):
        arr_token = tokenizer.sequences_to_matrix(np.array([testFinWordIndexes[i]]).tolist())
        test = np.concatenate((test, arr_token), axis=0) # Готовая верификационная выборка

    id_address = pd.read_excel('parsing_files/shops_rates.xlsx', usecols=['id', 'address']) # 
    shop_id = shop_reviews.id[0] # Берём id магазина
    shop_address = id_address.address[id_address.index[id_address.id == shop_id][0]] #Берём адрес по id
    
    # Загрузка архитектуры и весов нейронной сети
    model = load_model('input/model.h5')

    #Собираем список для подачи в сервис
    prediction = []
    id_address = pd.read_excel('parsing_files/shops_rates.xlsx', usecols=['id', 'address'])
    shop_id = shop_reviews.id[0] #Берём id магазина
    shop_address = id_address.address[id_address.index[id_address.id == shop_id][0]] #Берём адрес по id
    prediction.append([shop_id, shop_address])

    #Проходим по всем строкам df shop_reviews
    for i in range(len(shop_reviews)):
        #Получаем результаты распознавания класса
        currPred = model.predict(test[[i]])
        #Определяем номер распознанного класса
        currOut = np.argmax(currPred, axis=1)
        currOut = currOut +1
        prediction.append([shop_reviews.text[i], currOut])

    # prediction = [] #Собираем отчёт из txt для демонстрации
    # prediction.append([shop_id, shop_address])
    # for i in range(len(shop_reviews)):
    #     prediction.append([shop_reviews.text[i], shop_reviews.rate[i]])

    return prediction

print(prediction_list(shop_reviews))