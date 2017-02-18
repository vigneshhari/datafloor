from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Max
from pymongo import MongoClient
from sklearn.neighbors import KNeighborsClassifier
from django.http import HttpResponseRedirect
from userclassifier.models import ClassifierData
from sklearn.ensemble import RandomForestClassifier
import pickle
import nltk
import random
#from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier

from mlmarket.models import classifierspre

from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize
import time
import numpy as np
import random
import datetime
import time
import os
import csv




class classifier():

    def __init__(self,id,key,type,call,classifier,input = {},inputset = "" , outputset=""):
        self.id = id
        self.key = key
        self.type = type
        self.call = call
        self.input = input
        if(input == None): self.input={}
        self.inputset = inputset
        self.outputset = outputset
        self.classifier = classifier

    def trainRandomForest(self):
        classifierid = self.id
        key = self.key
        x_val = self.inputset.split(",")
        y_val = self.outputset
        client = MongoClient()
        db = client.userclassifier
        if (classifierid not in db.collection_names()):
            with open('upload/' + key) as csvfile:
                infos = db[classifierid]
                readCSV = csv.reader(csvfile, delimiter=',')
                readCSV = list(readCSV)
                headings = readCSV[0]

                datas = readCSV[1:]
            l = []
            for index, data in enumerate(datas):
                l.append(dict(zip(headings, data)))
            infos.insert_many(l)
        infos = db[classifierid]
        xunf = {}
        for i in x_val:
            xunf[i] = []

        file = open('upload/' + key + ".p", "wb")

        finaly = []

        for info in infos.find():
            finaly.append(info[y_val].encode('utf8'))
            looper = 0
            for i in x_val:
                try:
                    xunf[i].append(float(info[i].encode('utf8')))
                except Exception as e:
                    xunf[i].append(info[i].encode('utf8'))

        ykey = []

        for i in finaly:
            try:
                pp = float(i)
            except:
                ykey = list(set(finaly))
                finaly = [ykey.index(val) for val in finaly]
                break

        xkey = {}

        for x in xunf.keys():
            for i in xunf[x]:
                try:
                    pp = float(i)
                except:
                    keys = list(set(xunf[x]))
                    xkey[x] = keys
                    temp = [keys.index(val) for val in xunf[x]]
                    xunf[x] = temp
                    break
        finalx = []

        for i in range(0, len(list(xunf.values())[0])):
            temp = []
            for k in xunf.values():
                temp.append(k[i])
            finalx.append(temp)

        regr = RandomForestClassifier()
        regr.fit(finalx[:int(9 * len(finalx) / 10)], finaly[:int(9 * len(finaly) / 10)])

        pickle.dump(regr, file)
        pickle.dump(xkey, file)
        pickle.dump(ykey, file)

        acc = regr.score(finalx[int(9 * len(finalx) / 10):], finaly[int(9 * len(finalx) / 10):]) * 100


        return({"Accuracy": str(acc)})

    def trainKnn(self):
        classifierid = self.id
        key = self.key
        x_val = self.inputset.split(",")
        y_val = self.outputset
        client = MongoClient()
        db = client.userclassifier
        if (classifierid not in db.collection_names()):
            with open('upload/' + key) as csvfile:
                infos = db[classifierid]
                readCSV = csv.reader(csvfile, delimiter=',')
                readCSV = list(readCSV)
                headings = readCSV[0]

                datas = readCSV[1:]
            l = []
            for index, data in enumerate(datas):
                l.append(dict(zip(headings, data)))
            infos.insert_many(l)
        infos = db[classifierid]
        xunf = {}
        for i in x_val:
            xunf[i] = []

        file = open('upload/' + key + ".p", "wb")

        finaly = []

        for info in infos.find():
            finaly.append(info[y_val].encode('utf8'))
            looper = 0
            for i in x_val:
                try:
                    xunf[i].append(float(info[i].encode('utf8')))
                except Exception as e:
                    xunf[i].append(info[i].encode('utf8'))

        ykey = []

        for i in finaly:
            try:
                pp = float(i)
            except:
                ykey = list(set(finaly))
                finaly = [ykey.index(val) for val in finaly]
                break

        xkey = {}

        for x in xunf.keys():
            for i in xunf[x]:
                try:
                    pp = float(i)
                except:
                    keys = list(set(xunf[x]))
                    xkey[x] = keys
                    temp = [keys.index(val) for val in xunf[x]]
                    xunf[x] = temp
                    break
        finalx = []

        for i in range(0, len(list(xunf.values())[0])):
            temp = []
            for k in xunf.values():
                temp.append(k[i])
            finalx.append(temp)

        regr = KNeighborsClassifier(n_neighbors=3)
        regr.fit(finalx[:int(9 * len(finalx) / 10)], finaly[:int(9 * len(finaly) / 10)])

        pickle.dump(regr, file)
        pickle.dump(xkey, file)
        pickle.dump(ykey, file)

        acc = regr.score(finalx[int(9 * len(finalx) / 10):], finaly[int(9 * len(finalx) / 10):]) * 100


        return({"Accuracy": str(acc)})

    def classifyRandomForest(self):
        id = self.id
        key = self.key

        x_val = self.inputset.split(",")
        y_val = self.outputset
        temp = open('upload/' + key + ".p", "rb")
        regr = pickle.load(temp)
        xkey = pickle.load(temp)
        ykey = pickle.load(temp)

        inpdata = []


        for x in x_val:
            try:
                inpdata.append(xkey[x].index(self.input[x.strip()].encode("utf8")))
            except:
                inpdata.append(self.input.get(x.strip(),''))

        predictedval = regr.predict(inpdata)

        if (ykey == []):
            return({y_val: str(predictedval)})
        return({y_val: str(ykey[int(predictedval)])})

    def classifyKnn(self):
        id = self.id
        key = self.key

        x_val = self.inputset.split(",")
        y_val = self.outputset
        temp = open('upload/' + key + ".p", "rb")
        regr = pickle.load(temp)
        xkey = pickle.load(temp)
        ykey = pickle.load(temp)

        inpdata = []


        for x in x_val:
            try:
                inpdata.append(xkey[x].index((self.input[(x.strip())].encode("utf8"))))
            except:
                inpdata.append(self.input[(x.strip())])


        predictedval = regr.predict(inpdata)

        if (ykey == []):
            return({y_val: str(predictedval)})

        return({y_val: str(ykey[int(predictedval)])})

    def sentimentclassify(self):
        t1 = time.time()
        class VoteClassifier(ClassifierI):

            def __init__(self, *classifiers):
                self._classifiers = classifiers

        word_features5k_f = open("upload/word_features5k.pickle", "rb")
        word_features = pickle.load(word_features5k_f)
        word_features5k_f.close()

        save_classifier = open("upload/classifier.pkl", "rb")
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
            return mode(votes)

        def find_features(document):
            words = word_tokenize(document)
            features = {}
            for w in word_features:
                features[w] = (w in words)

            for i in words:
                try:
                    print(i, ' : ', features[i])
                except:
                    pass
            return features
        print(time.time() - t1)
        return({self.outputset : sentiment(self.input["sentence"])})

    def sentimenttrain(self):
        data = classifierspre.objects.all().filter(classifier=self.classifier)
        models = []
        for i in data:
            models = i.modelfiles.split(",")
        for i in models:
            data = open("upload/" + i.strip(), "rb")
            temp = pickle.load(data)
            savel = open("upload/" + self.key +  i.strip(), "wb")
            pickle.dump(temp,savel)
        return({"Accuracy" : " -%  Sucessfully Updated Trained Model"})

    def perform(self):
        if(self.type == "user"):
            funcs = {"trainRandomForest" : self.trainRandomForest , "trainKnn" : self.trainKnn  , "classifyRandomForest" : self.classifyRandomForest , "classifyKnn" : self.classifyKnn }
        else:
            funcs = {"classifysentiment" : self.sentimentclassify , "trainsentiment" :self.sentimenttrain }
        funcall =   self.call.strip() + self.classifier.strip()
        data =  (funcs[funcall]())
        return(data)





