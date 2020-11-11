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


models = {'LogReg':LogisticRegression, 'SVM':LinearSVC}

def train_model(corpus, model_type = 'LogReg', **kwargs):
	logger.info("--------------------------------------")
	logger.info(f"MODEL TYPE: {model_type}; CORPUS: {corpus}")
	model = models[model_type](**kwargs)
	model.fit(uni_and_bigram_tfidf_corpus, ratings)

	logger.info("Saving trained model object")
	with open(f'{model_type}.pkl', 'wb') as f:
		pickle.dump(model, f)


if __name__ == '__main__':
	
	# Setup CLI argument parser
	parser = argparse.ArgumentParser(description="Choose the type of model to train: LogReg or SVM")
	parser.add_argument('-m', '--model',
						help="Location of yelp reviews json data. Default: '/Users/kristiyan/Documents/MSiA 490 - Text Analytics/homework 3/yelp_data/yelp_academic_dataset_review.json'",
						default="LogReg", type=str)
	
	# Parse command line arguments
	args = parser.parse_args()
	logger.info(f'Successfully parsed command line arguments')


	#Loading the corpus that showed the best results: uni+bigram tfidf
	with open('uni_and_bigram_tfidf_corpus.pkl', 'rb') as f:
		uni_and_bigram_tfidf_corpus=pickle.load(f)

	with open('ratings.pkl', 'rb') as f:
		ratings=pickle.load(f)

	train_model(corpus=uni_and_bigram_tfidf_corpus, model_type=args.model)
	

