# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 18:35:44 2016

@author: Team-14
"""

import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
import re
import csv


victims =["Single"]*16325  #by Default all the cases were assumed to 
counter  = 1
with open('D:\\Semester 2\\TextMining\\CA\\osha.csv', 'rb') as csvfile:   #read the Osha File
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        #print (spamreader.line_num)
        for row in spamreader:
            #print row.index
            counter = spamreader.line_num
            ansList = []
            sample_text = row[3]
            custom_sent_tokenizer = PunktSentenceTokenizer(sample_text)
            new_word = replaceNumbers(sample_text)    #This is to replace the number that exist in the middle of the text that denotes fall meter or  some weight(Ex: 10 ft,50 ton)
            
            removedspaces = new_word.strip() #remove spaces 
            lastNumber = re.sub(r'\s(\d+)$',' replaced',removedspaces)  #this is to remove number that exist at the end of sentence (Freon 113-this is a chemical compund name)
            tokenized = custom_sent_tokenizer.tokenize(lastNumber)
            for i in tokenized:
                words = nltk.word_tokenize(i)
                tagged = nltk.pos_tag(words)
                namedEnt = nltk.ne_chunk(tagged, binary=True)
                hi = namedEnt.pos()
                for L in range(0,len(hi)):
                    newv = hi[L]
                    ans = newv[0]
                    if (ans[1]=="CD"):
                        #print "captured"
                        findNum_Mix_Words = re.findall(r'\d{1,}(rd|ft|nd|st|b)',ans[0])  #This is to remove numbers like 10ft,20dp
                        if len(findNum_Mix_Words) == 0 :
                            ansList.append("Multiple")                    
                        else:
                            print "skipping"
                            print ans[0]
            try:                
                if len(ansList) > 0:
                    victims.pop(counter)
                    victims.insert(counter,ansList)
            except Exception as e:
                print counter
                print(str(e))   
                        



def replaceNumbers(sample_text):
    new = re.sub(r'([0-9]+)(\s+)(Pound|Feet|ft|Floors|In|Scraper|Years|Percent|Ft|Degree|Volt|Days|Foot|Tons|Gallon|Inch|Rip)','replaced',sample_text)
    return new



#The below code is to write the answer captured into a file
with open("D:\\Semester 2\\TextMining\\CA\\ProperSet.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows([victims])



