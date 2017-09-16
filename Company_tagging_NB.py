import pandas as pd
import re
import sys
import ast
from sklearn.naive_bayes import MultinomialNB
from sklearn import preprocessing
import numpy as np
import nltk
from nltk.classify import NaiveBayesClassifier as nbc
from sklearn.feature_extraction.text import CountVectorizer
import csv

'''
---------------------------------------------Import Data --------------------------------------------------------------
'''

# df_training = pd.read_excel('/Users/Ankan/Documents/training_set.xlsx', sheetname = 'train')
# df_test = pd.read_excel('/Users/Ankan/Documents/training_set.xlsx', sheetname = 'test')
df_training = pd.read_excel('/Users/Ankan/Documents/training_set.xlsx', sheetname = 'train2')
df_test2 = pd.read_excel('/Users/Ankan/Documents/test_set.xlsx', sheetname = 'Sheet1')
# df_training.drop(df_training.columns[[0,1,2,3,4,5,6,8]], axis=1, inplace=True)
# df_test.drop(df_test.columns[[0,1,2,3,4,5,6,8]], axis=1, inplace=True)



'''
---------------------------------------------Classification [MultinomialNB()] Data ----------------------------------
'''

df_training = df_training.reindex(np.random.permutation(df_training.index))

count_vectorizer = CountVectorizer()
counts = count_vectorizer.fit_transform(df_training['Long Description'].values)

classifier = MultinomialNB()
targets = df_training['Sectors'].values
classifier.fit(counts, targets)


'''
---------------------------------------------Test Data --------------------------------------------------------------
'''

examples = []
for index, row in df_test2.iterrows():
    desc = row["Document"]
    examples.append(desc)
    print (desc)

example_counts = count_vectorizer.transform(examples)
predictions = classifier.predict(example_counts)


predictions = predictions.tolist()
print (predictions)

with open('/Users/Ankan/Documents/tags_newset.csv', 'w', newline='') as csvfile:
    datawriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)

for tag in predictions:

    with open('/Users/Ankan/Documents/tags_newset.csv', 'a', newline='') as csvfile:
        datawriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        datawriter.writerow([tag])


