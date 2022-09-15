"""
Prédit la race du chien sur l'image

Returns:
    predicted_label(string): race du chien sur l'image à img_path
"""

# Imports
import numpy as np
import keras
from keras.preprocessing import image
from keras.applications.xception import preprocess_input, decode_predictions
from PIL import Image


# Fonction
def get_predicted_label(img_path, model_path, class_list=None, img_size=224):
    """
    Prédit la race du chien sur l'image

    Args:
    img_path(string): path vers l'image

    model_path(string): path vers le modèle

    class_list(list): list des différentes races

    img_size(int): taille des côtés de l'image

    Returns:
    predicted_label
        - si class_list=None: predicted_label(int): le numero de la classe prédite
        - si class_list est renseigné: predicted_label(string) le label de la classe prédite
    """
    # Charge l'image
    img_input = image.load_img(img_path)

    # Resize l'image et convert en tensor
    img = img_input.resize((img_size,img_size))
    img_tensor = image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor = preprocess_input(img_tensor)

    # Charge le modèle
    reconstructed_model = keras.models.load_model(model_path)

    # Calcule les probabilités de chaque classe
    probas = reconstructed_model.predict(img_tensor)

    # Détermine la classe ayant la plus grande probabilité
    if class_list is None:
        predicted_label = np.argmax(probas)

    else:
        predicted_label = class_list[np.argmax(probas)]

    return predicted_label


# Exemple: obtenir une prédiction

# (img_path et model_path doivent être modifiés pour faire marcher ce code localement)

img_path = '/content/drive/My Drive/PStanford/data/images/Images/n02085620-Chihuahua/n02085620_3681.jpg'
model_path = "/content/drive/My Drive/PStanford/model_xception.h5"
img_size = 224
class_list = ["n02085620-Chihuahua",
            "n02085782-Japanese_spaniel",
            "n02085936-Maltese_dog",
            "n02086079-Pekinese",
            "n02086240-Shih-Tzu",
            "n02086646-Blenheim_spaniel",
            "n02086910-papillon",
            "n02087046-toy_terrier",
            "n02087394-Rhodesian_ridgeback",
            "n02088094-Afghan_hound"
            ]

get_predicted_label(img_path, model_path, class_list, img_size)