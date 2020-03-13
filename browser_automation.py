#import required modules
import os
import time
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from nltk.tokenize import sent_tokenize,word_tokenize
from selenium.webdriver.common.action_chains import ActionChains



#define driver
options = Options()
options.add_argument("--disable-notifications")
options.add_argument("--incognito")
driver = webdriver.Chrome("/home/pahul/Documents/chromedriver", chrome_options=options)
url="https://hub.lexile.com/analyzer"
#get url
driver.get(url)


#get all text files from folder
all_files = os.listdir("Story text files/") 
len(all_files)


#browser automation - Extract Text Score
iterator=0
#score=[]
all_files_left=[y for y in sorted(all_files) if y not in [x[0] for x in score if x[1]!="Not Defined"]]

for file in sorted(all_files_left):
    print("File Name: ",file)
    print("# File: ",iterator)
    
    score_value=0
    
    with open('Story text files/'+file, 'rt') as fd:
        text=fd.read().replace(".",". ")
    #truncate text with words more than 1000
    if len(word_tokenize(text))>1000:
        all_sentence=[]
        total_len=0
        for sentence in sent_tokenize(text):
            if (total_len+len(word_tokenize(sentence)))<1000:
                all_sentence.append(sentence)
                total_len=total_len+len(word_tokenize(sentence))
        text=(" ").join(all_sentence)
    else:
        all_sentence=[]
        for sentence in sent_tokenize(text):
            all_sentence.append(sentence)
        text=(" ").join(all_sentence)
            
        
    
    try:
        #focus on text area 
        driver.find_element_by_class_name("DraftEditor-editorContainer").click()
        #push text
        driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[2]/div/main/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/div').send_keys(text)
        
        #click analyze
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[2]/div/main/div/div[2]/div/div/div/div[2]/button').click()
        
        #get score
        time.sleep(5)
        score_value=driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[2]/div/main/div/div[2]/div/div/div/div[2]/h2/p').text
        print("Score: ",score_value)
        
        #start over
        driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[2]/div/main/div/div[2]/div/div/div/div[1]/div[2]/button[1]').click()
        #append text score
        score.append([file,score_value])
    
    except:
        score.append([file,"Not Defined"])
        
        #start over
        if driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[2]/div/main/div/div[2]/div/div/div/div[1]/div[2]/button[1]').text=='Upload Text File':
            driver.refresh()
            time.sleep(5)
        else:
            driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[2]/div/main/div/div[2]/div/div/div/div[1]/div[2]/button[1]').click()
                
    iterator=iterator+1

#save the score dataframe
pd.DataFrame([x for x in score if x[1]!="Not Defined"]).to_excel("Text_File_Score_Final.xlsx",index=False)


#Considering score for only those text file with number os senteneces >=2, since that is the minium number of senetences required for calculating lexile score.
score_label=pd.read_excel("Text_File_Score_Final.xlsx")
score_label.columns=["Text_File","Lexile Score Range"]

def get_number_of_sentences(file_name):
    
    with open('Story text files/'+file_name, 'rt') as fd:
        text=fd.read().replace(".",". ")
        
    number_of_sentences=len(sent_tokenize(text))
    
    return number_of_sentences

score_label["No of Sentences"]=score_label["Text_File"].apply(lambda x: get_number_of_sentences(x))
score_label_data=score_label[score_label["No of Sentences"]>=2].reset_index(drop=True)
score_label_data[["Text_File","Lexile Score Range"]].to_excel("dataset.xlsx",index=False)
