# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 12:18:15 2016

@author: Team - 14
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 19:11:25 2016

@author: Team 14
"""
from __future__ import print_function
import numpy as np
import pandas as pd
import nltk

import re


from sklearn import feature_extraction

import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.manifold import MDS
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.metrics import silhouette_score
from sklearn.metrics.pairwise import cosine_similarity
from nltk.cluster import GAAClusterer
from gensim import corpora, models, similarities 
from nltk.stem.snowball import SnowballStemmer
import csv
import string
from nltk.corpus import stopwords
stemmer = SnowballStemmer("english")

def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems

title_osha = []
category_list = []
nopunc = []
removStopwords = []

#The corresponding file name needs to be given here
with open('D:\\Semester 2\\TextMining\\CA\\FinaleLeftOut.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
          title_osha.append(row[3])  
          #category_list.append(row[0])
title_osha.pop(0) #Remove Column 
#category_list.pop(0)


for i in range(0,len(title_osha)):
    text_nopunc = title_osha[i].translate(string.maketrans("", ""), string.punctuation).lower()
    nopunc.append(title_osha[i].translate(string.maketrans("", ""), string.punctuation).lower())
   

stop = stopwords.words('english')

# Remove all these stopwords from the text

for i in range(0,len(nopunc)):
    removStopwords.append(" ".join(filter(lambda word: word not in stop, nopunc[i].split())))


#this to order the title
ranks = []
for i in range(0,len(removStopwords)):
    ranks.append(i)
    
    
#After doing initial data cleaning create TF-idf matrix
tfidf_vectorizer1Test = TfidfVectorizer(max_df=0.9, max_features=200000,
                                 min_df=0.05, stop_words='english',
                                 use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,3))
tfidf_matrix1Test = tfidf_vectorizer1Test.fit_transform(removStopwords)

# TDM Matrix (100 * 2727)
print(tfidf_matrix1Test.shape)

# Fitting a K-Means Model and evaluating its performance

from sklearn.cluster import KMeans
num_clusters = 4
km1 = KMeans(n_clusters=num_clusters, random_state=23)
km1.fit(tfidf_matrix1Test)
clusters1Test = km1.labels_.tolist()


array1 = np.array(clusters1Test)
silhouette_score(tfidf_matrix1Test, array1, metric='euclidean', sample_size=None, random_state=None)


terms = tfidf_vectorizer1Test.get_feature_names()

films = {'rank':ranks, 'title': removStopwords, 'cluster': clusters1Test }
frame = pd.DataFrame(films, index = [clusters1Test] , columns = ['rank','title', 'cluster'])

# Check the number of members of each cluster
frame['cluster'].value_counts()

vocab_frame = pd.DataFrame({'words': removStopwords}, index = removStopwords)
print ('there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')


#The below line of code is to assign the cluster formed into a seperate data frame so that it can be visualized using a word cloud
c0=[0]
cl = [1]
c2 = [2]
c3 = [3]
c4 = [4]
c5 = [5]
c6 = [6]
c7 = [7]
c8 = [8]
c9 = [9]
c10 = [10]
cluster0 = frame[frame.cluster.isin(c0)]
cluster1 = frame[frame.cluster.isin(cl)]
cluster2 = frame[frame.cluster.isin(c2)]
cluster3 = frame[frame.cluster.isin(c3)]
cluster4 = frame[frame.cluster.isin(c4)]
cluster5 = frame[frame.cluster.isin(c5)]
cluster6 = frame[frame.cluster.isin(c6)]
cluster7 = frame[frame.cluster.isin(c7)]
cluster8 = frame[frame.cluster.isin(c8)]
cluster9 = frame[frame.cluster.isin(c9)]
cluster10 = frame[frame.cluster.isin(c10)]

#temp = cluster0
#temp.append(cluster4)

#Write the entire cluster into a CSV file
pd.concat([cluster0,cluster1,cluster2,cluster3,cluster4,cluster5,cluster6,cluster7,cluster8,cluster9,cluster10]).to_csv("D:\\Semester 2\\TextMining\\CA\\FullCLuster_LeftOut.csv",sep=",")

#Write each cluster into a seperate file
cluster0.to_csv("D:\\Semester 2\\TextMining\\CA\\cluster0.csv",sep=",")
cluster1.to_csv("D:\\Semester 2\\TextMining\\CA\\cluster1.csv",sep=",")
cluster2.to_csv("D:\\Semester 2\\TextMining\\CA\\cluster2.csv",sep=",")
cluster3.to_csv("D:\\Semester 2\\TextMining\\CA\\cluster3.csv",sep=",")
cluster4.to_csv("D:\\Semester 2\\TextMining\\CA\\cluster4.csv",sep=",")
cluster5.to_csv("D:\\Semester 2\\TextMining\\CA\\cluster5.csv",sep=",")
cluster6.to_csv("D:\\Semester 2\\TextMining\\CA\\cluster6.csv",sep=",")
cluster7.to_csv("D:\\Semester 2\\TextMining\\CA\\cluster7.csv",sep=",")
cluster8.to_csv("D:\\Semester 2\\TextMining\\CA\\cluster8.csv",sep=",")
cluster9.to_csv("D:\\Semester 2\\TextMining\\CA\\cluster9.csv",sep=",")
cluster10.to_csv("D:\\Semester 2\\TextMining\\CA\\cluster10.csv",sep=",")





    

