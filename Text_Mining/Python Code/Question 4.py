# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 20:13:24 2016

@author: Team 14
"""
'''
Import all required packages
'''
import nltk
from nltk.tokenize import PunktSentenceTokenizer
import pandas as pd
import re
Df = pd.DataFrame()
# Load the osha file to a dataframe
Df=pd.read_excel("G:/Sem 2/Text Mining/Project/osha.xlsx",names=['DocID','Title','Summary','Abstract','Fatality'])
finalDF = pd.DataFrame()
temp_DF = pd.DataFrame()
Activities = pd.DataFrame()

# Function to process the input data and retrieve activities involved by the victims
def process_content(tokenized,DocID):
    try:
        wordlist=[]
        for i in tokenized:
            words = nltk.word_tokenize(i)  # tokenize each sentence to word
            tagged = nltk.pos_tag(words)   # tag parts of speech for each word
            chunkGram = r"""Chunk: {<RB>*<VBG>+<DT>*<IN>*<JJ>*(<NN>|<NNS>)+}""" # Regular expression to match with the patterns
            chunkParser = nltk.RegexpParser(chunkGram)
            chunked = chunkParser.parse(tagged)
            for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Chunk'): # retrive all activities named as chunk
                action=subtree.pos()
                words=[]
                wordstr=""
                for K in range(0,len(action)):
                    hi=action[K]
                    w = hi[0]
                    wordstr=wordstr + w[0] +" "
                words.append(wordstr)
                if (len(words)>0):
                    words.insert(1,DocID)
                    wordlist.append(words)
		return wordlist
    except Exception as e:
        print(str(e))
        return wordlist
        

for index, row in Df.iterrows():
    sample_text=row['Summary']
    DocID=row['DocID']
    custom_sent_tokenizer = PunktSentenceTokenizer(sample_text)
    tokenized = custom_sent_tokenizer.tokenize(sample_text)
    m = process_content(tokenized,DocID)
    df=pd.DataFrame(m,columns=["Activity","DocID"])
    finalDF=pd.concat([finalDF,df])
    
for index,row in finalDF.iterrows():
    sample_text1=row['Activity']
    DocID=row['DocID']
    findpattern = re.findall(r'not\s.*',sample_text1)
    if (len(findpattern) ==0):
        temp_DF=pd.DataFrame({'Text':[sample_text1],'DOCID':[DocID]})
        Activities = pd.concat([Activities, temp_DF])
# Load all the activities into a csv
Activities.to_csv("Activities.csv")          
    