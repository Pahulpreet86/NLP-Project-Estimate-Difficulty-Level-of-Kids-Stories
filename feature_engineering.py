#import required modules
import os
import numpy as np
import pandas as pd
from math import sqrt
import en_core_web_sm
from nltk.tokenize import sent_tokenize,word_tokenize


dataframe=pd.read_excel("dataset.xlsx")

def get_all_text(file_name):
    
    with open('Story text files/'+file_name, 'rt') as fd:
        text=fd.read().replace(".",". ")
        
    return text

def average_word_length(text):
    number_words=len(word_tokenize(text))
    number_of_char=0
    for word in word_tokenize(text):
        number_of_char=number_of_char+len(word)
    avg_word_len=number_of_char/number_words
    return avg_word_len


def syllable_count_per_word(word):
    #lower 
    word=word.lower()
    #vowels
    vowels = "aeiouy"
    number_of_syllables = 0

    if word[0] in vowels:
        number_of_syllables=number_of_syllables+1

    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            number_of_syllables=number_of_syllables+1

    if word.endswith("e"):
        number_of_syllables=number_of_syllables-1

    if number_of_syllables == 0:
        number_of_syllables=number_of_syllables+1

    return number_of_syllables

def avg_syllable_count_per_word(text):
    
    words_list_number_of_syllables=[]
    
    words=word_tokenize(text)
    
    total_number_of_words=len(words)
    
    for word in words:
        number_of_syllables=syllable_count_per_word(word)
        words_list_number_of_syllables.append(number_of_syllables)

    return (sum(words_list_number_of_syllables)/total_number_of_words)


def no_complex_words(text):
    words=word_tokenize(text)
    complex_words=[word for word in words if syllable_count_per_word(word)>2 ]
    return len(complex_words)



#Readilibility Score

def Automated_Readability_Index(text):
    
    number_of_sentence=len(sent_tokenize(text))
    number_of_words=len(word_tokenize(text))

    number_of_char=0
    for word in word_tokenize(text):
        number_of_char=number_of_char+len(word)
    
    avg_no_of_char_per_words=(number_of_char/number_of_words)
    
    avg_no_of_words_per_sentence=(number_of_words/number_of_sentence)
    
    ARI=(4.71*avg_no_of_char_per_words)+(0.5*avg_no_of_words_per_sentence)-21.43
    
    return ARI
    

    
def Flesch_Reading_Ease(text):
    
    total_words=len(word_tokenize(text))
    total_sentences=len(sent_tokenize(text))
    
    total_syllables=sum([syllable_count_per_word(word) for word in word_tokenize(text)])
    
    
    avg_no_of_words_per_sentence=(total_words/total_sentences)
    
    avg_no_of_syllables_per_words=(total_syllables/total_words)
    
    
    FRE= 206.835 - (1.015*avg_no_of_words_per_sentence) - (84.6*avg_no_of_syllables_per_words)
    
    return FRE


def FleschKincaid_Grade_Level(text):
    
    total_words=len(word_tokenize(text))
    total_sentences=len(sent_tokenize(text))
    
    total_syllables=sum([syllable_count_per_word(word) for word in word_tokenize(text)])
    
    
    avg_no_of_words_per_sentence=(total_words/total_sentences)
    
    avg_no_of_syllables_per_words=(total_syllables/total_words)
    
    
    FGL= (0.39*avg_no_of_words_per_sentence) + (11.8*avg_no_of_syllables_per_words) -15.59
    
    
    return FGL


def Coleman_Liau_Index(text):
        
    number_of_sentence=len(sent_tokenize(text))
    number_of_words=len(word_tokenize(text))

    number_of_char=0
    for word in word_tokenize(text):
        number_of_char=number_of_char+len(word)
    
    avg_no_of_char_per_words=(number_of_char/number_of_words)
    
    avg_no_of_sentence_per_words=(number_of_sentence/number_of_words)
    
    
    CLI=(5.89*avg_no_of_char_per_words)-(30*avg_no_of_sentence_per_words)-15.8
    
    return CLI
    

def Gunning_Fog_Index(text):
    
    total_words=len(word_tokenize(text))
    total_sentences=len(sent_tokenize(text))
    total_complex_words=no_complex_words(text)
    
    
    avg_no_of_words_per_sentence=(total_words/total_sentences)
    
    avg_no_complex_words_per_words=(total_complex_words/total_words)
    
    GFI= 0.4*(avg_no_of_words_per_sentence+(100*avg_no_complex_words_per_words))
    
    return GFI

def SMOG_Index(text):
    
    total_sentences=len(sent_tokenize(text))
    total_complex_words=no_complex_words(text)
    
    SI=sqrt(total_complex_words+(30/total_sentences))+3
    
    return SI


def Linsear_Write(text):
    
    text=(" ").join(text.split()[:100])
    
    words=word_tokenize(text)
    no_easy_words=len([word for word in words if syllable_count_per_word(word)<=2 ])
    no_hard_words=len([word for word in words if syllable_count_per_word(word)<=3 ])
    
    words_wt=(1*no_easy_words)+(3*no_hard_words)
    
    LW=words_wt/len(sent_tokenize(text))
    
    return LW

#https://en.wikipedia.org/wiki/Dale%E2%80%93Chall_readability_formula
def Dale_Chall_Readability(text):
    total_sentences=len(sent_tokenize(text))
    total_words=len(word_tokenize(text))
    
    #Number of EasyWords
    with open('DaleChallEasyWordList.txt', 'rt') as fd:
        easy_words=fd.read().split("\n")
        
    total_difficult_words=len([y for y in word_tokenize(text) if y.lower() not in easy_words])

    DCR=0.1579*((total_difficult_words/total_words)*100)+0.0496*(total_words/total_sentences)
    
    return DCR

#dict for pos tags and their frequency
def get_pos_count(pos_tags):
    
    data_dict={'ADJ': 0,
     'ADP': 0,
     'ADV': 0,
     'AUX': 0,
     'CONJ': 0,
     'CCONJ': 0,
     'DET': 0,
     'INTJ': 0,
     'NOUN': 0,
     'NUM': 0,
     'PART': 0,
     'PRON': 0,
     'PROPN': 0,
     'PUNCT': 0,
     'SCONJ': 0,
     'SYM': 0,
     'VERB': 0,
     'X': 0,
     'SPACE': 0}
    
    for pos_tag in pos_tags:
        data_dict[pos_tag]=data_dict[pos_tag]+1
            
    return data_dict
    
#creating features from text in the files

#get all text for feature creation
dataframe["Content"]=dataframe["Text_File"].apply(lambda x: get_all_text(x))

#Number of Words
dataframe["Word_Count"]=dataframe["Content"].apply(lambda x: len(word_tokenize(x)))

#Number of Sentences
dataframe["Sentence_Count"]=dataframe["Content"].apply(lambda x: len(sent_tokenize(x)))


#Average Word Length
dataframe["Avg_Word_Length"]=dataframe["Content"].apply(lambda x: average_word_length(x))


#Average no of words per sentence
dataframe["Avg_No_Word_Per_Sentence"]=dataframe["Word_Count"]/dataframe["Sentence_Count"]


#Average syllable count per word
dataframe["Avg_Syllable_Count_Per_Word"]=dataframe["Content"].apply(lambda x: avg_syllable_count_per_word(x))


#Number of Complex Words
dataframe["No_Complex_Words"]=dataframe["Content"].apply(lambda x: no_complex_words(x))



#Number of Common Words
with open('google-10000-english.txt', 'rt') as fd:
    most_common_words=fd.read().split("\n")
    

dataframe["No_Common_Words"]=dataframe["Content"].apply(lambda x: len([y for y in word_tokenize(x) if y.lower() in most_common_words]))

#Average Number of Complex Words Per Sentence
dataframe["Avg_No_Complex_Words_Per_Sentence"]=dataframe["No_Complex_Words"]/dataframe["Sentence_Count"]

#Average Number of Simple Words Per Sentence
dataframe["Avg_No_Simple_Words_Per_Sentence"]=dataframe["No_Common_Words"]/dataframe["Sentence_Count"]


#Ratio of complex words/common words
dataframe["Ratio_Complex_Words_Per_Common_Words"]=dataframe["No_Complex_Words"]/dataframe["No_Common_Words"]



#Number of EasyWords
with open('DaleChallEasyWordList.txt', 'rt') as fd:
    easy_words=fd.read().split("\n")
    

dataframe["No_Easy_Words"]=dataframe["Content"].apply(lambda x: len([y for y in word_tokenize(x) if y.lower() in easy_words]))
dataframe["No_Difficulty_Words"]=dataframe["Content"].apply(lambda x: len([y for y in word_tokenize(x) if y.lower() not in easy_words]))


#Average Number of Easy Words Per Sentence
dataframe["Avg_No_Easy_Words_Per_Sentence"]=dataframe["No_Easy_Words"]/dataframe["Sentence_Count"]

#Average Number of Difficulty Words Per Sentence
dataframe["Avg_No_Difficulty_Words_Per_Sentence"]=dataframe["No_Difficulty_Words"]/dataframe["Sentence_Count"]


#Ratio of difficult words/Easy words
dataframe["Ratio_Difficulty_Words_Per_Easy_Words"]=dataframe["No_Difficulty_Words"]/dataframe["No_Easy_Words"]


dataframe["Automated_Readability_Index"]=dataframe["Content"].apply(lambda x: Automated_Readability_Index(x))

dataframe["Flesch_Reading_Ease"]=dataframe["Content"].apply(lambda x: Flesch_Reading_Ease(x))

dataframe["FleschKincaid_Grade_Level"]=dataframe["Content"].apply(lambda x: FleschKincaid_Grade_Level(x))

dataframe["Coleman_Liau_Index"]=dataframe["Content"].apply(lambda x: Coleman_Liau_Index(x))

dataframe["Gunning_Fog_Index"]=dataframe["Content"].apply(lambda x: Gunning_Fog_Index(x))

dataframe["SMOG_Index"]=dataframe["Content"].apply(lambda x: SMOG_Index(x))

dataframe["Linsear_Write"]=dataframe["Content"].apply(lambda x: Linsear_Write(x))

dataframe["Dale_Chall_Readability"]=dataframe["Content"].apply(lambda x: Dale_Chall_Readability(x))


#get pos features

post_tags_dataframe=[]
nlp = en_core_web_sm.load()
for itr in range(len(dataframe)):
    print(itr)
    
    text_file_name=dataframe["Text_File"].loc[itr]
    text=dataframe["Content"].loc[itr]
    
    pos_tags=get_pos_count([x.pos_ for x in nlp(text)])
    
    pos_tags["Text_File"]=text_file_name
    
    post_tags_dataframe.append(pos_tags)

    
post_tags_dataframe=pd.DataFrame(post_tags_dataframe)
post_tags_dataframe=post_tags_dataframe[['Text_File','ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'CONJ', 'DET', 'INTJ', 'NOUN','NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SPACE', 'SYM', 'VERB', 'X']]

#add post tags features to the dataframe
dataframe_comb=dataframe.set_index("Text_File").join(post_tags_dataframe.set_index("Text_File")).reset_index()
dataframe_final=dataframe_comb[["Text_File",'Word_Count', 'Sentence_Count', 'Avg_Word_Length', 'Avg_No_Word_Per_Sentence', 'Avg_Syllable_Count_Per_Word', 'No_Complex_Words', 'No_Common_Words', 'Avg_No_Complex_Words_Per_Sentence', 'Avg_No_Simple_Words_Per_Sentence', 'Ratio_Complex_Words_Per_Common_Words', 'No_Easy_Words', 'No_Difficulty_Words', 'Avg_No_Easy_Words_Per_Sentence', 'Avg_No_Difficulty_Words_Per_Sentence', 'Ratio_Difficulty_Words_Per_Easy_Words', 'Automated_Readability_Index', 'Flesch_Reading_Ease', 'FleschKincaid_Grade_Level', 'Coleman_Liau_Index', 'Gunning_Fog_Index', 'SMOG_Index', 'Linsear_Write', 'Dale_Chall_Readability', 'ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'CONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SPACE', 'SYM', 'VERB', 'X','Lexile Score Range']]


dataframe_final.to_excel("dataset_modelling.xlsx",index=False)

