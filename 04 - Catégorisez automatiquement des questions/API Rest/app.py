"""
REST API Prédiction de tags StackOverflow

Input: Json contenant le titre et le corps d'une question StackOverflow

2 points d'entrée:
- /proba: retourne la probabilité de chacun des 50 tags les plus commun pour la question soumise
- /prediction: retourne les tags prédits pour la question soumise
"""

# Imports
import pickle
import numpy as np
import uvicorn
import nltk
import spacy
from fastapi import FastAPI
from pydantic import BaseModel
from preprocessing import normalize_corpus
import preprocessing

# éléments nécessaires aux fonctions de preprocessing
nltk.download('stopwords')
spacy.cli.download("en_core_web_sm")
nlp = spacy.load('en_core_web_sm')
#tokenizer = ToktokTokenizer()
stopword_list = nltk.corpus.stopwords.words('english')

class stackoverflow_question(BaseModel):
    """
    StackOverflow question to predict must follow this format
    """
    Title: str
    Body: str

app = FastAPI()

# Charge le pipeline sklearn (TF-IDF + MultiOutputClassifier avec Reg Log)
with open("ressources/model.pkl", "rb") as f:
    model = pickle.load(f)

# Charge la liste des classes (venant du MultiLabelBinarizer)
with open("ressources/classes.pkl", "rb") as f:
    classes = pickle.load(f)


@app.post('/proba', summary="Retourne la probabilité des 50 tags les plus communs")
def get_proba(data: stackoverflow_question):
    """
    Endpoint permettant d'obtenir la probabilité de chacun des 50 tags
    les plus communs sur StackOverflow pour la question

    Args:
        data (stackoverflow_question): Titre et Corps de la question StackOverflow

    Returns:
        JSON: probabilité pour chaque tag
    """

    received = data.dict()

    concat_inputs = received["Title"] + " " + received["Body"]

    normalized_inputs = normalize_corpus(concat_inputs)

    pred_proba = model.predict_proba([normalized_inputs])

    zip_proba = zip(
        classes, 
        np.vstack(pred_proba)[:,1]
        )

    proba = dict(zip_proba)

    return proba


@app.post('/prediction', summary="Retourne une liste des tags prédits")
def get_prediction(data: stackoverflow_question):
    """
    Endpoint permettant d'obtenir une list des tags prédits (P>0.5)

    Args:
        data (stackoverflow_question): Titre et Corps de la question StackOverflow

    Returns:
        JSON: tags prédits
    """
    received = data.dict()

    concat_inputs = received["Title"] + " " + received["Body"]

    normalized_inputs = normalize_corpus(concat_inputs)

    pred_tags = model.predict([normalized_inputs])   

    zip_tags = zip(
        classes, 
        pred_tags[0])

    predicted_tags = dict(zip_tags)

    list_predicted = [k for k,v in predicted_tags.items() if v == 1]

    predicted = { 'predicted_tags' : list_predicted}

    return predicted


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=4000, debug=True)