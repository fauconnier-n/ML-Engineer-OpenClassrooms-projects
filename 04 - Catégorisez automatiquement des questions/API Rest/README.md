# REST API tags StackOverflow

For a StackOverflow question and its title:
- the probabilities of the top 50 tags on website
- the list of the predicted tags (P>0.5)

Made with [FastAPI](https://fastapi.tiangolo.com/), deployed on [Heroku](https://www.heroku.com/). 

## Endpoints, Swagger & documentation

Access the Swagger & doc [HERE](https://stackoverflow-tags-pred.herokuapp.com/docs)  

Get the probabilities for each tag at this endpoint (POST) : 
https://stackoverflow-tags-pred.herokuapp.com/proba

Get a list of the predicted tags at this endpoint (POST) : 
https://stackoverflow-tags-pred.herokuapp.com/prediction

## The model behind the predictions
A simple sklearn MultiOutputClassifier with logistic regressions trained on TF-IDF.
