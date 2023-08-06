# Topic Sentiment Model

## Sentiment Analysis component for Formsflow.ai

One of the unique features of Formsflow.ai framework is Sentiment Analysis.  A
form designer can add text component with sentiment analysis enabled when creating
forms with associated topics. Based on the input responses of the user Formsflow.ai
 process sentiment associated with user responses. A detailed visualisation is being
 rendered in Insights section of Formsflow.ai which shows the overall sentiment and
  detailed sentiment analysis based on the topics specified by the form designer.

## Libraries used

- Spacy
- NLTK

## Machine Learning model 

This project groups the input sentences into specific topic categories and
uses custom named entity classification, our machine learning model identifies
words belonging to a particular topic. This custom named entity recognition is
 done using Spacy library.  One of top of it we do aspect based
sentiment analysis for each given topics. For this currently we have leveraged 
NLTK vader library.

