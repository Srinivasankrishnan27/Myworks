# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 21:45:15 2016

@author: Madhwesh
"""

from nltk import pos_tag
from nltk import *
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import stem
from sklearn import tree
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split
import pandas as pd
import os
from nltk.tokenize import PunktSentenceTokenizer
import csv
from os import path
import string
import nltk
import re

#read data
trainAcc = pd.read_csv("E:\\Lecture Notes - Sem 2\\Text Mining\\CA\\MsiaAccidentCases.csv")
trainTitle = trainAcc['title_2']

    
    
#tokenizing 
tokenized =[]    
for i in range(0,len(trainTitle)):
    tokens = word_tokenize(trainTitle[i])
    tokenized .append(tokens)

#tagging    
tag = []   
for i in range(0, len(tokenized)):
    a = pos_tag(tokenized[i]) 
    tag.append(a)
    
#stopword removal
stop = stopwords.words('english')


def traverse(o, tree_types=(list, tuple)):
    if isinstance(o, tree_types):
        for value in o:
            for subvalue in traverse(value, tree_types):
                yield subvalue
    else:
        yield o
        
        
removStopwords = []
for w in traverse(tag):
    if w not in stop:
        removStopwords.append(w)
        
        
        
r=[]
objects = ''
for i in tag:
    #print i
    #    for j in i:
     #       print j 
    regx = "NP : {<IN><.*>*(<NN>|<NNS>)*}"
    parser=nltk.RegexpParser(regx)
    result_exp=parser.parse(i)
    for k in result_exp.subtrees(filter=lambda x: x.label()== 'NP'):
        objects=' '
        for j in k:
            if j[1] =='NN' or j[1] == 'NNS':
                objects+=j[0] + ' '
                print objects+" ``"
        r.append(objects)    
                

        
   import csv
with open('output_293objects.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(r)   

##################################################################
##OSHA DATA#######################################################
##################################################################
trainAcc_osha = pd.read_csv("E:\\Lecture Notes - Sem 2\\Text Mining\\CA\\osha.csv")
trainTitle_osha = trainAcc_osha['title_2']
#tokenizing 
tokenized_osha =[]    
for i in range(0,len(trainTitle_osha)):
    tokens1 = word_tokenize(trainTitle_osha[i])
    tokenized_osha.append(tokens1)
#tagging    
tag_osha = []   
for i in range(0, len(tokenized_osha)):
    a = pos_tag(tokenized_osha[i]) 
    tag_osha.append(a)




r_osha=[]
objects = ''
count=0
for i in tag_osha:
    flag=0
    regx = "NP : {<IN><.*>*(<NN>|<NNS>)*}"
    parser=nltk.RegexpParser(regx)
    result_exp=parser.parse(i)
    for k in result_exp.subtrees(filter=lambda x: x.label()== 'NP'):
        objects=' '
        for j in k:
            if j[1] =='NN' or j[1] == 'NNS':
                objects+=j[0] + ' ' 
                flag=1
                                #print objects+" ``"
    if flag==0:
         objects="NULL"
         count=count+1
    r_osha.append(objects)   
print count        
        

df = pd.DataFrame(r_osha)
df.to_excel("E:\\Lecture Notes - Sem 2\\Text Mining\\CA\\final_object_list.xls")
