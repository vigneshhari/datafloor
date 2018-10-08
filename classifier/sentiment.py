import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize
import time


from nltk.classify import ClassifierI

class VoteClassifier(ClassifierI):
    pass

word_features5k_f = open("pickled_algos/word_features5k.pickle", "rb")
word_features = pickle.load(word_features5k_f)
word_features5k_f.close()

save_classifier = open("classifier.pkl","rb")
voted_classifier = pickle.load(save_classifier)
save_classifier.close()

def sentiment(text):
    feats = find_features(text)
    return classify(feats)
def classify(features):
        votes = []
        for c in voted_classifier._classifiers:
            v = c.classify(features)
            votes.append(v)
        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        print(conf)
        return mode(votes)

def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

