# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 20:44:07 2016

@author: Ritika
"""

import nltk,operator,re,collections
import pandas as pd
from pytagcloud import create_tag_image, make_tags, LAYOUTS
from pytagcloud.lang.counter import get_tag_counts
body_parts = ['finger', 'head', 'hand', 'leg', 'abdomen']
gender = ['male','female']
def get_from_title(title_pos):
    #create regular expression to parse the Title to get occupation
    grammar="NP: {^<NN>*}"
    cp=nltk.RegexpParser(grammar)
    result=cp.parse(title_pos)
    occupations=''
    #get the chunks from the identified pattern
    for i in result.subtrees(filter=lambda x: x.label() == 'NP'):
        occupations=''
        for j in i:
            if j[0] not in body_parts and j[0] not in gender:
                occupations+=j[0]+' '
    return occupations
#Get the first sentence from the summary  
def get_first_sentence(my_string):
    count =0
    split_string = my_string.split(' ')
    first_sentence = []
    for ele in split_string:
        if ele is not "":
            if '.' in ele:
                count = -1
                first_sentence.append(ele)
            else:
                if count == -1:  
                    if ele[0].isupper():
                        break
                    else:
                        count =0
                        first_sentence.append(ele) 
                else:
                     first_sentence.append(ele)                
    return ' '.join(first_sentence)

def get_from_summary(summary):
    occupations=''
    line = get_first_sentence(summary)
    line_token = nltk.word_tokenize(line)
    line_pos=nltk.pos_tag(nltk.word_tokenize(str(line)))
    grammar="NP: {<CD><DT><.*>+?(<IN>|<VBD>)}"
    cp=nltk.RegexpParser(grammar)
    result=cp.parse(line_pos)
    for i in result.subtrees(filter=lambda x: x.label() == 'NP'):
        for j in i:
                occupations+=j[0]+' '
    if occupations is None:
        for token in line_token:
            if token=='operator' or token=='operating' or token=='operation':
                occupations = 'operator'
                
    return occupations			   
    
summary_1=[]
title_1=[]
occ_list = []
case_id = []
k=0
for cases in open("osha.csv","r+"):
    flag=0
    k=k+1
    if k<17000:
        id,title,summary,c1,c2=cases.split(",")
        #convert the title text to lower and tokenize
        title_words = nltk.word_tokenize(title.lower())
        #DO POS tagging for the title tokens
        title_pos = nltk.pos_tag(title_words)
        #Fetch occupation from Title
        occupations = get_from_title(title_pos)
        #if occupation not found in title or is employee, worker or burn, check for occupation in Sumary
        if occupations is None or occupations in ['employee ','worker ', 'burn  ']:
            occupations_from_summary = get_from_summary(summary)
            #If found and not employee, work or burn set the occupation to the one fetched from summary
            if occupations_from_summary is not None and occupations_from_summary not in ['employee ', 'worker ','burn '] :
                occupations = occupations_from_summary
                print occupations
        #Append Case ID and occupation to the list
        case_id.append(id)
        occ_list.append(occupations)
data = zip(case_id,occ_list)
#create a data frame and export occupations to CSV
df=pd.DataFrame(data,columns=['CaseID','Occupation'])
df.to_csv('occupations_osha.csv')
    