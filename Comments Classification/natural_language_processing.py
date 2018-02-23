# Natural Language Processing

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Import dataset
dataset = pd.read_csv('train.csv')

# CLeaning the texts
import re
import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
corpus = []

for i in range(0, 500) :
    # Only keep letters
    # First Step : Kept All the letters
    review = re.sub('[^a-zA-Z]', ' ', dataset['comment_text'][i])    
    
    # Second Step : Change all letters to lower case 
    review = review.lower()
    
    # Third Step: Remove unwanted words
    review = review.split()
    
    # Fourth Step : Stemming - Taking root of the word 
    ps = PorterStemmer()
    
    review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
    
    # joining back list of clean words

    review = ' '.join(review)
    corpus.append(review)
    
# Creating Bag of Words model    
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=1000)    
X = cv.fit_transform(corpus).toarray()
y = dataset.iloc[:500,2:8].values



# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Importing the Keras libraries and packages
import keras
# Sequential module is used to initialise artificial neural network        
from keras.models import Sequential
# Add different layers to artificial neural network     
from keras.layers import Dense

# Initializing the ANN
classifier = Sequential()

# Adding input layer and the first hidden layer
classifier.add(Dense(output_dim=1003,init='uniform',activation='relu',input_dim=1000))

# Adding the second hidden layer
classifier.add(Dense(output_dim=1003,init='uniform',activation='relu'))

# Adding the output layer for multiclass change output dim and activation='softmax'
classifier.add(Dense(output_dim=6,init='uniform',activation='softmax'))

# Compiling the ANN
classifier.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])

# Fitting ANN to the Training set
classifier.fit(X_train,y_train,batch_size=10,epochs=100)


# Create your classifier here

# Predicting the Test set results
y_pred = classifier.predict(X_test)
np.savetxt('output.csv',y_pred,delimiter=',')
y_pred = (y_pred > 0.5)
# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)