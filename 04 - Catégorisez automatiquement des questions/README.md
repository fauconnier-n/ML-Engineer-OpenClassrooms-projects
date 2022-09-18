# A REST API that returns the predicted tags of a StackOverflow question

For a StackOverflow question and its associated title, returns:
- the probabilities of the top 50 most popular tags on the website
- the list of the predicted tags (output a list of every tag for which P>0.5)

Made with [FastAPI](https://fastapi.tiangolo.com/), deployed on [Heroku](https://www.heroku.com/). 

## API REST, Endpoints, Swagger & documentation

All the files for the API are in [/API REST](https://github.com/fauconnier-n/ML-Engineer-OpenClassrooms-projects/tree/main/04%20-%20Cat%C3%A9gorisez%20automatiquement%20des%20questions/API%20Rest)

Access the Swagger & doc [HERE](https://stackoverflow-tags-pred.herokuapp.com/docs)  

Get the probabilities for each tag at this endpoint (POST) : 
https://stackoverflow-tags-pred.herokuapp.com/proba

Get a list of the predicted tags at this endpoint (POST) : 
https://stackoverflow-tags-pred.herokuapp.com/prediction

## The model behind the predictions
A simple sklearn MultiOutputClassifier with logistic regressions trained on TF-IDF.

## Notebooks
- [notebook_exploration.ipynb](https://github.com/fauconnier-n/stackoverflow_app/blob/master/Notebooks/notebook_exploration.ipynb) contains all the data cleaning, pre-processing, EDA, and some (failed) attempts at Dimentional Reduction
- [notebook_test.ipynb](https://github.com/fauconnier-n/stackoverflow_app/blob/master/Notebooks/notebook_test.ipynb) contains feature extractions (TF-IDF, Word2Vec, BERT, Universal Sentence Encoder) supervised and unsupervised learning (Latent Dirichlet Allocation). The more advanced feature extractions methods would probably offer better performances used with a deep neural network instead of the MultiOutputClassifier.

**This project was made as part of my Machine Learning Engineer & Data Science degree at OpenClassrooms & CentraleSupélec.**

nb. OpenClassrooms is the largest online education platform in France, and delivers state recognised University level diplomas.

Therefore, **comments and Markdown cells are in French** (mandatory at OpenClassrooms).
