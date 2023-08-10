import os
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import numpy as np
from tensorflow import image

class Model():
    def __init__(self, classes, model_path=os.path.join(os.getcwd(), 'model', 'model_kue_manado.h5')):
        self.model_path = model_path
        self.class_names = classes

    def predict(self, img):
        model = load_model(self.model_path)
        img = img_to_array(img)
        img = image.resize(img, size=(224, 224))
        img = np.expand_dims(img, axis=0) / 255.
        prediction = model.predict(img)
        predicted = np.argmax(prediction)
        probabilites = prediction[0][predicted]
        prediction = self.class_names[predicted]
        return prediction, probabilites