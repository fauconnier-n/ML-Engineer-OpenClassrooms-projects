# Classification of dog pictures using Deep Learning

The goal of this project is to use Deep Learning and Tranfert Learning to classify images.
 
The dataset is the [Stanford Dogs Dataset](http://vision.stanford.edu/aditya86/ImageNetDogs/).
It contains 120 different races of dog (predicted label), but we only use 10 in this notebook.
 
The **selected model is Xception pretrained (Transfert Learning) on imagenet, and offers an Accuracy of ~84%.**

## Files
- [Notebook](https://github.com/fauconnier-n/ML-Engineer-OpenClassrooms-projects/blob/main/05%20-%20Classez%20des%20images%20%C3%A0%20l'aide%20d'algorithmes%20de%20Deep%20Learning/FAUCONNIER_Nicolas_1_notebook_062022.ipynb) : contains Data Cleaning, pre-processing, Data Augmentation, training of multiple models (with and without Tranfert Learning), Hyperparameter Optimization, and Fine Tuning (nb. pre-processing and data augmentation could have been done using keras layers directly in the models; the method used here is deprecated)
- [Python file](https://github.com/fauconnier-n/ML-Engineer-OpenClassrooms-projects/blob/main/05%20-%20Classez%20des%20images%20%C3%A0%20l'aide%20d'algorithmes%20de%20Deep%20Learning/FAUCONNIER_Nicolas_2_programme_062022.py) : a Python function that returns the predicted race from a given image


**This project was made as part of my Machine Learning Engineer & Data Science degree at OpenClassrooms & CentraleSupélec.**

Therefore, **comments and Markdown cells are in French** (mandatory at OpenClassrooms). Don't hesitate to contact me if you have any question.

nb. OpenClassrooms is the largest online education platform in France, and delivers state recognised University level diplomas.




