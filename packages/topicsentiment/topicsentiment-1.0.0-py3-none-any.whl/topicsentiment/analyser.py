import spacy
import os

from pathlib import Path
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize


def load_model_output(text):
    """Function to load the trained machine learning model for inference and
    return the output as the necessary entities and topics for each element
    param text: The input text blob being entered by user
    """
    # uncomment when working in linux and remove subsequent two lines
    # nlp = spacy.load("../models/quick-spacy/")
    model_path = Path(__file__).parent.absolute() / "models/quick-spacy/"
    nlp = spacy.load(model_path)
    doc = nlp(text)
    entity = [ent.text for ent in doc.ents]
    labels = [ent.label_ for ent in doc.ents]
    return entity, labels


def analyser(text):
    """
    A input pipeline which returns for a given text blob, output of
    aspect based sentiment analaysis as list of entities with associated
    sentiment.
    Usage:
        >> analyser(text="awesome staff and tea was epic.")
            {'staff': 'pos, 'tea': 'pos'}
    :param text: The input text blob which is being used by model
    :param topics: Optional and update as required
    """

    entity, labels = load_model_output(text)

    full_sentence = []
    full_text = text.split(".")

    for i in range(len(entity)):
        temp = ''
        for t in full_text:
            if(len(full_text)>=1):
                if entity[i] in t.lstrip():
                    temp +=t
        full_sentence.append(temp)

    sid = SentimentIntensityAnalyzer()
    full_text = full_sentence
    sentiment_output = {}

    for i, t in enumerate(full_text):
        ss = sid.polarity_scores(t)

        if ss["compound"] >= 0.15:
            sentiment_output[labels[i]] = "positive"
        elif ss["compound"] <= -0.01:
            sentiment_output[labels[i]] = "negative"
        else:
            sentiment_output[labels[i]] = "neutral"

    response = {}

    response["sentiment"] = sentiment_output
    response["staff"] = sentiment_output.get("staff")
    response["facility"] = sentiment_output.get("facility")
    response["location"] = sentiment_output.get("location")
    response["service"] = sentiment_output.get("service")
    response["overall_sentiment"] = overall_sentiment(text)

    return response


def overall_sentiment(text):
    # tokenize_text = tokenize.sent_tokenize(text)
    # print(tokenize_text)
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(text)
    for k in sorted(ss):
        # print('{0}: {1}, '.format(k, ss[k]), end='')
        if ss["compound"] >= 0.15:
            return "positive"
        elif ss["compound"] <= -0.01:
            return "negative"
        else:
            return "neutral"
