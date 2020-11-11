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

from preprocessing import *


# Setup logging
logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
						datefmt='%m/%d/%Y %I:%M:%S %p',
						level=logging.INFO)

logger = logging.getLogger(__file__)


models = {'LogReg':LogisticRegression, 'SVM':LinearSVC}

def predict(texts):
	
	# Loading the model object
	with open('SVM.pkl', 'rb') as f:
		model=pickle.load(f)

	# Loading the tfidf vectorizer
	with open('tfidf_vectorizer.pkl', 'rb') as f:
		tfidf_vectorizer=pickle.load(f)


	preprocessed_texts = preprocess(texts)
	preprocessed_texts_strings = [" ".join(text) for text in preprocessed_texts]

	tfidf_texts = tfidf_vectorizer.transform(preprocessed_texts_strings)

	predictions = model.predict(tfidf_texts)
	keys = ['label_'+str(i) for i in range(1,len(predictions)+1)]

	predictions_dict = dict(zip(keys, predictions))

	with open('result.json', 'w') as fp:
		json.dump(predictions_dict, fp)


if __name__ == '__main__':
	
	# Setup CLI argument parser
	parser = argparse.ArgumentParser(description="Makes predictions for texts and saves to result.json")
	parser.add_argument('-f', '--file',
						help="File containing reviews to predict for. Default: '/Users/kristiyan/Documents/MSiA 490 - Text Analytics/homework 3/yelp_data/yelp_academic_dataset_review.json'",
						default="texts.txt", type=str)
	
	# Parse command line arguments
	args = parser.parse_args()
	logger.info(f'Successfully parsed command line arguments')

	with open(args.file, 'r', encoding='utf8') as filehandle:
		content = filehandle.readlines()
	texts = [x.strip() for x in content if x.strip()] 
	
	predict(texts)
	

