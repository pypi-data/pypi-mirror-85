import os
import shutil
import DuckDuckGoImages as ddg
import tensorflow_hub as hub
from tensorflow.nn import softmax
from tensorflow.keras import layers
from tensorflow.keras import losses
from tensorflow.keras import optimizers
from tensorflow.keras import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from quicklearning.classification.image.model import Model

balanced = (
    hub.KerasLayer("https://tfhub.dev/google/efficientnet/b0/feature-vector/1", trainable=False),
    224,
    optimizers.RMSprop(learning_rate=0.001)
)

def fit(input_model, epochs, classes=[], data_folder="./images", batch_size=32, validation_split=0.2, verbose=False):
    (transfer_learning_layer, size, optimizer) = input_model

    _download_data(data_folder, classes)
    model = _create_model(transfer_learning_layer, size, optimizer, classes)
    
    model = Model(model, size, classes=classes, data_folder=data_folder, batch_size=batch_size, validation_split=validation_split, verbose=verbose)
    model.fit(epochs)
    return model

def _download_data(data_folder, classes):
    _create_folder(data_folder)
    for item in classes:
        if not os.path.exists('{}/{}'.format(data_folder, item)):
            ddg.download(item, folder='{}/{}'.format(data_folder, item), thumbnails=True, parallel=True)

def _create_model(transfer_learning_layer, size, optimizer, classes):
    model = Sequential([
        transfer_learning_layer,
        layers.Dense(len(classes), activation=softmax)
    ])
    if len(classes) <= 2:
        loss = losses.BinaryCrossentropy(from_logits=True)
    else:
        loss = losses.CategoricalCrossentropy(from_logits=True)

    model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])
    model.build([None, size, size, 3])
    return model

def _create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def _remove_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder, ignore_errors=True)