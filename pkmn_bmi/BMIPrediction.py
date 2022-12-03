# Neural Network to predict the BMI of a pokemon based on its stats

from keras.callbacks import EarlyStopping
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Input, Dense
from keras.optimizers import Adam
import matplotlib.pyplot as plt
import numpy as np
import tkinter
import pdb
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

def main():
    # Load data
    print('Loading data...')
    basePokemonCSV = np.loadtxt(os.path.join(ROOT, 'PokemonData.csv'), dtype=str, delimiter=',')
    BMIPokemonCSV = np.loadtxt(os.path.join(ROOT, 'pokemon.csv'), dtype=str, delimiter=',')
    pokemonTestData = np.loadtxt(os.path.join(ROOT, 'pokemon_data_test.csv'), dtype=str, delimiter=',')

    x_train = np.array(basePokemonCSV[1:, 4:10], dtype=float)
    t_train = np.array(BMIPokemonCSV[1:, 2:4], dtype=float)

    x_test = np.array(pokemonTestData[1:, 4:10], dtype=float)
    t_test = np.array(pokemonTestData[1:, 10:12], dtype=float)

    BMI_train = np.array([(float(i[1]) / (float(i[0])**2), 4) for i in t_train])
    BMI_test = np.array([(float(i[1]) / (float(i[0])**2), 4) for i in t_test])
    # pdb.set_trace()

    # Create neural network
    model = Sequential()
    model.add(Input(shape=6))
    model.add(Dense(units=100,activation='relu',name='hidden1'))
    model.add(Dense(units=100,activation='sigmoid',name='hidden2'))
    model.add(Dense(units=100,activation='relu',name='hidden3'))
    model.add(Dense(units=100,activation='sigmoid',name='hidden4'))
    model.add(Dense(units=2,activation='linear',name='output'))
    model.summary()

    input("Press <enter> to continue")

    model.compile(
        loss='categorical_crossentropy',
        optimizer=Adam(learning_rate=0.0001),
        metrics=['accuracy']
    )

    callback = EarlyStopping(
        monitor='loss',
        min_delta=1e-2,
        patience=10,
        verbose=1
    )

    # Network training
    history = model.fit(x_train, t_train,
        epochs=1000,
        batch_size=10,
        callbacks=[callback],
        verbose=1
    )

    # Network test
    train_metrics = model.evaluate(x_train, t_train, verbose=0)
    print('TRAINING DATA')
    print(f'loss = {train_metrics[0]:0.4f}')
    print(f'accuracy = {train_metrics[1]:0.4f}')

    test_metrics = model.evaluate(x_test, t_test, verbose=0)
    print('TESTING DATA')
    print(f'loss = {test_metrics[0]:0.4f}')
    print(f'accuracy = {test_metrics[1]:0.4f}')

    train_labels = model.predict(x_train, verbose=0)
    test_labels = model.predict(x_test, verbose=0)

    BMI_train_pred = np.array([(float(i[1]) / (float(i[0])**2), 4) for i in train_labels])
    BMI_test_pred = np.array([(float(i[1]) / (float(i[0])**2), 4) for i in test_labels])

    x_train_sums = np.array([np.sum(x) for x in x_train])
    x_test_sums = np.array([np.sum(x) for x in x_test])

    # pdb.set_trace()

    # plt.figure(1)
    # plt.plot(x_train_sums, BMI_train, 'r.', x_test_sums, BMI_test, 'b.')
    # plt.title("Targets")
    # plt.xlabel("BASE STAT TOTALS")
    # plt.ylabel("BMI")
    # plt.show()

    # plt.figure(1)
    # plt.plot(x_train_sums, BMI_train_pred, 'r.', x_test_sums, BMI_test_pred, 'b.')
    # plt.title("Predictions")
    # plt.xlabel("BASE STAT TOTALS")
    # plt.ylabel("BMI")
    # plt.show()


if __name__ == "__main__":
    main()