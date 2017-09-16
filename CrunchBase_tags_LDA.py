import xlrd
import nltk
import csv
from nltk.tokenize import RegexpTokenizer
from stopwords import get_stopwords
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import sys

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stopwords('en')
a = ['/' ,'s' ,'n' ,' ','may', '9', '11', '2016', 'brooklyn', 'cruise', 'terminal', 'brooklyn', 'york', 'thus', 'far',
     'disrupt', 'ny', 've', 'seen', 'handshake', 'stalemate', 'iab', 'randall', 'rothenberger', 'adblocker', 'till',
     'faida', 've', 'seen', 'submit', 'startup', 'careers', 'contact', 'us', 'privacy', 'policy', 'disclaimer',
     'activate', 'facebook', 'messenger', 'news', 'bot', 'subscribed', 'bot', 'will', 'send', 'digest', 'trending',
     'stories', 'day', 'can', 'also', 'customize', 'types', 'stories', 'sends', 'click', 'button', 'subscribe', 'wait',
     'new', 'facebook', 'message', 'tc', 'messenger', 'news', 'bot', 'thanks', 'tc', 'team','cost','costs','text','com',
     'we','users','user','people','global','you','city','state','country']

do_not_include = ['CC','CD','DT','IN','JJS','LS','MD','PDT','POS','RB','RBR','RBS','UH',
                  'VB','VBD','VBG','VBN','VBP','VBZ','WDT','WP','WRB','NNP']

# include = ['NN','NNP','NNS','PRP','PRP$']
for b in a:
    en_stop.append(b)


# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()


wb = xlrd.open_workbook('/Users/Ankan/Documents/Data For Nucleus/TagTree1.xlsx')
ws = wb.sheet_by_name('Sheet2')
texts = []
counter = 0
for i in range(0,5723):
    doc_title = []
    doc_set = []
    doc_set = ws.cell_value(i,0)
    print(doc_set)
    # doc_title = ws.cell_value(i,0)
    # print(doc_title)
    ppt_text = []
    corrected_text = []
    # loop through document list
    tokens = tokenizer.tokenize(doc_set)
    print (tokens)

    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if not i in en_stop]

    ppt_text = nltk.pos_tag(stopped_tokens)
    for word, pos in ppt_text:
        if pos not in do_not_include:
            corrected_text.append(word)
            print (word,pos)
    # stem tokens
    # stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
    # add tokens to list
    texts.append(corrected_text)
    # texts = corrected_text
    # print (texts)
    counter +=1
    print(counter)
    print (corrected_text)


print (texts)

#
# line = str()
# line = " ".join(texts)
# print (line)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)

print(dictionary)

# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
n_topics=20
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=n_topics, id2word=dictionary, passes=100)

# print(ldamodel.print_topics(num_topics=10, num_words=8))


topics_matrix = ldamodel.show_topics(formatted=False, num_words=10)

lda = ldamodel
bagofterms = []

fl = open('/Users/Ankan/Documents/Data For Nucleus/topic_CB.csv', 'w')

writer = csv.writer(fl)


## word lists
for i in range(0, n_topics):
    temp = lda.show_topic(i,10)
    terms = []
    for term in temp:
        terms.append(term)
    print("Top 10 terms for topic #" + str(i) + ": "+ ", ".join([i[0] for i in terms]))
    writer.writerow(terms)
    bagofterms += terms

print(bagofterms)


## word clouds
from os import path
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def terms_to_wordcounts(t, multiplier=1000):
    return  " ".join([" ".join(int(multiplier*i[1]) * [i[0]]) for i in t])

wordcloud = WordCloud(font_path="/Library/Fonts/Times New Roman.ttf", background_color="black").generate(terms_to_wordcounts(bagofterms))

plt.imshow(wordcloud)
plt.axis("off")
plt.savefig("terms1")

plt.close()


## topic-words vectors: topics vs. words
from sklearn.feature_extraction import DictVectorizer

def topics_to_vectorspace(n_topics, n_words=100):
    rows = []
    for i in range(0, n_topics):
        temp = lda.show_topic(i, n_words)
        row = dict(((i[1],i[0]) for i in temp))
        rows.append(row)

    return rows

vec = DictVectorizer()

X = vec.fit_transform(topics_to_vectorspace(n_topics))
X.shape

#PCA

## PCA Topics
from sklearn.decomposition import PCA

pca = PCA(n_components=2)

X_pca = pca.fit(X.toarray()).transform(X.toarray())

plt.figure()
for i in range(X_pca.shape[0]):
    plt.scatter(X_pca[i, 0], X_pca[i, 1], alpha=.5)
    plt.text(X_pca[i, 0], X_pca[i, 1], s=' ' + str(i))

plt.title('PCA Topics of Wiki')
plt.savefig("pca_topic")

plt.close()

#PCA Words
X_pca = pca.fit(X.T.toarray()).transform(X.T.toarray())

plt.figure()
for i, n in enumerate(vec.get_feature_names()):
    plt.scatter(X_pca[i, 0], X_pca[i, 1], alpha=.5)
    plt.text(X_pca[i, 0], X_pca[i, 1], s=' ' + n, fontsize=8)

plt.title('PCA Words of Wiki')
plt.savefig("pca_words")

plt.close()

## hierarchical clustering
from scipy.cluster.hierarchy import linkage, dendrogram

plt.figure(figsize=(12,6))
R = dendrogram(linkage(X_pca))
plt.savefig("dendro")

plt.close()

## correlation matrix
from scipy.spatial.distance import pdist, squareform

cor = squareform(pdist(X.toarray(), metric="euclidean"))

plt.figure(figsize=(12,6))
R = dendrogram(linkage(cor))
print(R)
plt.savefig("corr")

plt.close()

# ## network
# import networkx as nx
#
# from sklearn.pipeline import make_pipeline
# from sklearn.preprocessing import Normalizer
#
# pca_norm = make_pipeline(PCA(n_components=20), Normalizer(copy=False))
#
# X_pca_norm = pca_norm.fit(X.toarray()).transform(X.toarray())
#
# cor = squareform(pdist(X_pca_norm, metric="euclidean"))
#
# G = nx.Graph()
#
# for i in range(cor.shape[0]):
#     for j in range(cor.shape[1]):
#         if i == j:
#             G.add_edge(int(i), int(j), {"weight":0})
#         else:
#             if cor[i,j] == 0:
#                 cor[i, j] = 1
#             else:
#                 G.add_edge(int(i), int(j), {"weight":1.0/cor[i,j]})
#
# edges = [(i, j) for i, j, w in G.edges(data=True) if w['weight'] > .8]
# edge_weight=dict([((u,v,),int(d['weight'])) for u,v,d in G.edges(data=True)])
#
# #pos = nx.graphviz_layout(G, prog="twopi") # twopi, neato, circo
# pos = nx.spring_layout(G)
#
# nx.draw_networkx_nodes(G, pos, node_size=100, alpha=.5)
# nx.draw_networkx_edges(G, pos, edgelist=edges, width=1)
# nx.draw_networkx_edge_labels(G, pos ,edge_labels=edge_weight)
# nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')
#
#
# plt.savefig("network")
#
# nx.write_gml(G,"/Users/Ankan/PycharmProjects/Pyprogrammes/network_wiki.gml")
#
# plt.close()
#
# ## visualization of the topics
# import pyLDAvis
# import pyLDAvis.gensim
# pyLDAvis.enable_notebook()
# vis_data = pyLDAvis.gensim.prepare(ldamodel, corpus, dictionary)
# pyLDAvis.save_html(vis_data, 'output_filename.html')
