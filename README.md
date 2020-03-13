# NLP Project: Estimate Difficulty Level of Kids Stories

# Project Report
  

## 1.  Business Domain
    

-   Freadom is an adaptive mobile reading platform that helps parents with children aged 3 - 10, learn to read in English by instilling a daily reading habit.
    
-   It provides parents and teachers curated and levelised stories, activities, quizzes and daily positive news to enjoy with the child.
    

  

## 2.  Business Problem
    

-   The stories in the Freadom app need to be simple and easy to understand. To ensure that students gain most from each reading session, it is imperative to make sure that the stories which the app recommends to students are at his level of proficiency.
    
-   If there is conflict between the level of proficiency of students with that of the story which we are recommending to students, it will not lead to any learning or improvement in reading proficiency.
    

  

## 3.  Analytical Overview
    

### -   Target Definition:
    

1.  Develop a model which estimates the relative difficulty level of the stories based on their text data only.
    
2.  To determine if the story is at the appropriate level, multiple factors are taken into account such as overall length of the story, average length of the sentences in the story and whether the words used are simple or complex etc.
    

  

### -   Inputs:
    

1.  556 text files extracted from stories used in the Freedom app.
    
2.  All the text Files are of variable length.
    

  
  

## 4.  Solution Description
    

### -   Lexile Text Measure
    

1.  A Lexile reader measure represents a person’s reading ability on the Lexile scale. A Lexile text measure represents a text’s difficulty level on the Lexile scale.
    
2.  The reader’s score on the test is reported as a Lexile measure from a low of 0L to a high of 2000L. When readers score at or below 0L, a BR (Beginning Reader) code is displayed on their report.
    

  

### -   Initial Approach:
    

1.  The initial approach was to use [Lexile Titles Database™](https://lexile.com/for-researchers/) for training the model and then use the model to predict the Lexile Text Measure for the given stories. But this dataset is available on request.
    
2.  The [lexile analyzer tool](https://hub.lexile.com/analyzer) is based on the [Lexile Titles Database™](https://lexile.com/for-researchers/) and provides lexile score for the text entered.
    
3.  The above tool was used for acquiring the lexile score for the given input text files.
    

  

### -   Data Labelling:
    

1.  The data labeling process was automated through selenium web driver.

![](https://lh5.googleusercontent.com/sJAPpe1CmlpT63W14C1dukB6SQzOX4QMAkSVyI3xldVlNFtx5NNXV8KJBBEtmwAlE2FjS1qiIARdgb16vQqmZMnbeS3ptv6nYUFQ3h4Nhz7cYLrLMcoB4z0YaA_N_rJ5t7F9YR3R)

2.  The [lexile analyzer tool](https://hub.lexile.com/analyzer) requires at least 2 sentences in the entered text, and sufficient text length for calculation [up to 1000 words].
    
3.  The final labelled dataset consisted of lexile score range for 548 text files.
    
4.  The Lexile score for text files was then mapped to grade levels as follows on the basis of the mapping defined [here](https://www.scholastic.com/parents/books-and-reading/reading-resources/book-selection-tips/lexile-levels-made-easy.html):
    

	1.  Lexile Score Range: BR190L - 400L -> Grade < 2
	    
	2.  Lexile Score Range: 410L - 1000L -> Grade 2 - Grade 4
	    
	3.  Lexile Score Range: 1010L - 1400L -> Grade > 4
	    

  

### -   Feature Engineering:
    

1.  A total of 42 text-based features were created for the 548 input text files consisting of features as follows:
    

  

#### 1.  Text Analysis Based features:
    

1.  Number of Words
    
2.  Number of Sentences
    
3.  Average Word Length
    
4.  Average no of words per sentence
    
5.  Average syllable count per word
    
6.  Number of Complex Words
    
7.  Number of Common Words
    
8.  Average Number of Complex Words Per Sentence
    
9.  Average Number of Simple Words Per Sentence
    
10.  Ratio of complex words/common words
    
11.  Number of Easy words
    
12.  Number of Difficult words
    
13.  Average Number of Easy Words Per Sentence
    
14.  Average Number of Difficulty Words Per Sentence
    
15.  Ratio of Difficult words/Easy words
    

  

#### 2.  Text Readability Score:
    

1.  Automated Readability Index
    
2.  Flesch Reading Ease
    
3.  FleschKincaid Grade Level
    
4.  Coleman Liau Index
    
5.  Gunning Fog Index
    
6.  SMOG Index
    
7.  Linsear Write
    
8.  Dale Chall Readability
    

#### 3.  POS Tags (Distribution): distribution (frequency) of the following tags in the text files
    

1.  ADJ
    
2.  ADP
    
3.  ADV
    
4.  AUX
    
5.  CCONJ
    
6.  CONJ
    
7.  DET
    
8.  INTJ
    
9.  NOUN
    
10.  NUM
    
11.  PART
    
12.  PRON
    
13.  PROPN
    
14.  PUNCT
    
15.  SCONJ
    
16.  SPACE
    
17.  SYM
    
18.  VERB
    
19.  X
    

  

### -   Algorithms and Feature Selection:
    

  

#### 1.  Baseline Model:
    

 - Algorithm: Random Forest Classifier
  
 -   Number of Features: 42
  
 -   Evaluation: Cross-Validation [4 fold]
  
 - Scoring Metric: Accuracy
 -   Results: 88.5 %

    

  

#### 2.  Model 1:
    

 - Algorithm: Random Forest Classifier
   
  
 -  Feature Selection Method: SelectFromModel (feature importance based method)
   
 -  Number of Selected Features: 16
   
   
     
   
 -  Evaluation: Cross-Validation [4 fold]
   
 -  Scoring Metric: Accuracy
   
 -  Results: 88.87 %

    

  

#### 3.  Model 2:
    

-  Algorithm: Random Forest Classifier
    
-  Feature Selection Method: SelectFromModel (feature importance based method)
    
-  Number of Selected Features: 16
    
-  Parameter Tuning: RandomizedSearchCV
    
-  Tuned Parameter:  n_estimators= 600, min_samples_split= 12, min_samples_leaf= 4, max_features= sqrt, max_depth= 4, bootstrap= False
    
-  Evaluation: Cross-Validation [4 fold]
    
-  Scoring Metric: Accuracy
    
-  Results: 89.42 %
    

  

####  4.  Model 3:
    

-  Algorithm: Support Vector Machine
    
-  Number of Features: 42
    
-  Evaluation: Cross-Validation [4 fold]
    
-  Scoring Metric: Accuracy
    
-  Results: 83.21 %
    

  

#### 5.  Model 4:
    

-  Algorithm: XGBoost Classifier
    
-  Number of Features: 42
    
-  Evaluation: Cross-Validation [4 fold]
    
-  Scoring Metric: Accuracy
    
-  Results: 87.96 %
    

  

#### 6.  Model 5:
    

-   Algorithm: XGBoost Classifier
    
-   Feature Selection Method: SelectFromModel (feature importance based method)
    
-   Number of Selected Features: 11
    
-   Evaluation: Cross-Validation [4 fold]
    
-   Scoring Metric: Accuracy
    
-   Results: 88.69 %
    

  

#### 7.  Model 6:
    

-  Algorithm: XGBoost Classifier
    
-  Feature Selection Method: SelectFromModel (feature importance based method)
    
-  Number of Selected Features: 11
    
-  Parameter Tuning: RandomizedSearchCV
    
-  Tuned Parameter:  subsample= 0.8, n_estimators= 200, min_child_weight= 8, max_depth= 12, learning_rate= 0.01, colsample_bytree= 0.8
    
-  Evaluation: Cross-Validation [4 fold]
    
-  Scoring Metric: Accuracy
    
-  Results: 89.78 %
    

  

#### 8.  Model Results: Summary
    
| Model          | Algorithm                | Meta Description                                                                                                                    | Accuracy |
|----------------|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------|----------|
| Baseline Model | Random Forest Classifier | Baseline Model with All Features                                                                                                    | 88.5 %   |
| Model 1        | Random Forest Classifier | Baseline Model with 16 Selected Features using SelectFromModel (feature importance based method)                                    | 88.5 %   |
| Model 2        | Random Forest Classifier | Baseline Model with 16 Selected Features SelectFromModel (feature importance based method)and Parameter Tuning using RandomSearchCV | 89.42 %  |
| Model 3        | Support Vector Machine   | All Features                                                                                                                        | 83.21 %  |
| Model 4        | XGBoost Classifier       | All Features                                                                                                                        | 87.96 %  |
| Model 5        | XGBoost Classifier       | 11 Selected Features using SelectFromModel (feature importance based method)                                                        | 88.69 %  |
| Model 6        | XGBoost Classifier       | 11 Selected Features using SelectFromModel (feature importance based method) and Parameter Tuning using RandomSearchCV              | 89.78 %  |
  
  

### -   Results:
    

#### 1.  Final Model Description:
    

-  Algorithm: XGBoost Classifier
    
-  Number of Selected Features: 11
    
-  Selected Features and Importance:
	    
	| Feature                           | Importance |
	|-----------------------------------|------------|
	| NOUN                              | 0.254066   |
	| FleschKincaid_Grade_Level         | 0.143781   |
	| Automated_Readability_Index       | 0.133037   |
	| Avg_No_Complex_Words_Per_Sentence | 0.112143   |
	| Word_Count                        | 0.072617   |
	| No_Difficulty_Words               | 0.063537   |
	| SCONJ                             | 0.062241   |
	| PRON                              | 0.053438   |
	| NUM                               | 0.045221   |
	| Avg_Word_Length                   | 0.030411   |
	| Coleman_Liau_Index                | 0.029509   |4.  Tuned Parameter:  subsample= 0.8, n_estimators= 200, min_child_weight= 8, max_depth= 12, learning_rate= 0.01, colsample_bytree= 0.8
    
-  Evaluation: Cross-Validation [4 fold]
    
-  Scoring Metric: Accuracy
    
-  Results: 89.78 %
    

  

### -   Sources of Error:
    

1.  The text data for each file is an excerpt from the story. Since the features for the model are based on text data such as number of sentences, number of words per sentence, there is a significant effect of them on the model predicted labels. Therefore, the predicted labels may change for the same story but a different excerpt.
    

  

2.  Due to the small size of the dataset, there is a class imbalance:
    

	  
	|  Grade Level       | Lexile Score Range |
	|-------------------|--------------------|
	| Grade < 2         | 62                 |
	| Grade 2 - Grade 4 | 456                |
	| Grade > 4         | 30                 |
	
	The model doesn’t have enough examples to find discriminative features that will be used to generalise.

  

## 5.  Code Files and Description:
    

  
| Code File                             | Language | Description                                                                          | Input                                            | Output                 |
|---------------------------------------|----------|--------------------------------------------------------------------------------------|--------------------------------------------------|------------------------|
| browser_automation.py                 | python   | automated data labeling process through selenium web driver for the input text files | text files [Story text files/*txt]               | dataset.xlsx           |
| feature_engineering.py                | python   | feature engineering from text data                                                   | dataset.xlsx, text files [Story text files/*txt] | dataset_modelling.xlsx |
| Feature Selection and Modelling.ipynb | python   | Features Selection and Modelling                                                     | dataset_modelling.xlsx                           |                        |


## 6.  References
    

-   **Lexile Text Measure:**
    

	1.  [https://lexile.com/for-researchers/](https://lexile.com/for-researchers/)
	    
	2.  [http://cdn.lexile.com/m/uploads/downloadablepdfs/WhatDoestheLexileMeasureMean.pdf](http://cdn.lexile.com/m/uploads/downloadablepdfs/WhatDoestheLexileMeasureMean.pdf)
	    
	3.  [https://www.scholastic.com/parents/books-and-reading/reading-resources/book-selection-tips/lexile-levels-made-easy.html](https://www.scholastic.com/parents/books-and-reading/reading-resources/book-selection-tips/lexile-levels-made-easy.html)
    

  

-   **Readability Index:**
    

	1.  [http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.659.7114&rep=rep1&type=pdf](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.659.7114&rep=rep1&type=pdf)
	    
	2.  [https://en.wikipedia.org/wiki/Dale%E2%80%93Chall_readability_formula](https://en.wikipedia.org/wiki/Dale%E2%80%93Chall_readability_formula)

