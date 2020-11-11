import argparse
import logging
import logging.config
import os
import json
import pandas as pd
import multiprocessing
import pickle
import gensim
import subprocess
import matplotlib.pyplot as plt

from gensim import utils
from nltk.corpus import stopwords
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.svm import LinearSVC


# Setup logging
logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
						datefmt='%m/%d/%Y %I:%M:%S %p',
						level=logging.INFO)

logger = logging.getLogger(__file__)


if __name__ == '__main__':
	
	# Reading in the pickled preprocessed reviews with bigrams
	with open('preprocessed_reviews_strings.pkl', 'rb') as f:
		preprocessed_reviews_strings = pickle.load(f)

	# Unigrams BOW
	count_vectorizer = CountVectorizer(lowercase=False, ngram_range =(1,1), max_df = .5, min_df = 100)
	unigram_bow_corpus = count_vectorizer.fit_transform(preprocessed_reviews_strings)

	# Uni + bigrams BOW
	count_vectorizer = CountVectorizer(lowercase=False, ngram_range =(1,2), max_df = .5, min_df = 100)
	uni_and_bigram_bow_corpus = count_vectorizer.fit_transform(preprocessed_reviews_strings)

	# TFIDF unigrams
	tfidf_vectorizer = TfidfVectorizer(lowercase=False, ngram_range =(1,1), max_df = .5, min_df = 100)
	unigram_tfidf_corpus = tfidf_vectorizer.fit_transform(preprocessed_reviews_strings)

	# TFIDF unigrams and bigrams
	tfidf_vectorizer = TfidfVectorizer(lowercase=False, ngram_range =(1,2), max_df = .5, min_df = 100)
	uni_and_bigram_tfidf_corpus = tfidf_vectorizer.fit_transform(preprocessed_reviews_strings)

	# Saving the tfidf_vectorizer as part of the preprocessing pipeline
	with open('tfidf_vectorizer.pkl', 'wb') as f:
		pickle.dump(tfidf_vectorizer, f)

	# Saving the 4 corpuses
	with open('uni_and_bigram_bow_corpus.pkl', 'wb') as f:
		pickle.dump(uni_and_bigram_bow_corpus, f)

	with open('unigram_bow_corpus.pkl', 'wb') as f:
		pickle.dump(unigram_bow_corpus, f)

	with open('unigram_tfidf_corpus.pkl', 'wb') as f:
		pickle.dump(unigram_tfidf_corpus, f)

	with open('uni_and_bigram_tfidf_corpus.pkl', 'wb') as f:
		pickle.dump(uni_and_bigram_tfidf_corpus, f)
