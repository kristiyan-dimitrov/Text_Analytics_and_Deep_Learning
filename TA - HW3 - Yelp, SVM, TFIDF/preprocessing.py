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


def access_yelp_reviews(datapath, n_reviews=500_000):
	
	# Initialize empty output
	reviews = []
	ratings = []
	counter = 0

	with open(datapath, 'r', encoding='utf8') as filehandle:
		
		while counter < n_reviews:

			line = json.loads(filehandle.readline())

			if counter % 99_999 == 0:
				logger.info(f'Accessed {counter} reviews')
				
			reviews.append(line['text'])
			ratings.append(line['stars'])

			counter += 1
			
	return reviews, ratings
  

def remove_stopwords(tokenized_sentence:str):

	return [word for word in tokenized_sentence if word not in stopwords.words('english')]


def preprocess_text(text:str):
	"""Converts text to sentences; tokenizes sentences; removes all stopword tokens"""
	
	# Preprocess each sentence converting it into a list of lower case tokens, which are not too long or too short
	tokenized_text = gensim.utils.simple_preprocess(text)
	
	# Remove any tokens which are stop words
	no_stops = remove_stopwords(tokenized_text)
		
	return no_stops


def preprocess(reviews):

	logger.info(f"Beginning multiprocessing of reviews with {multiprocessing.cpu_count()} parallel processes")
	
	pool=multiprocessing.Pool(multiprocessing.cpu_count())
	preprocessed_reviews = pool.map(preprocess_text, reviews)
	pool.close()

	return preprocessed_reviews


if __name__ == '__main__':
	# Setup CLI argument parser
	parser = argparse.ArgumentParser(description="Preprocesses 500,000 yelp reviews and saves them to pickle file; Preprocessing is tokenization and removing stop words.")
	parser.add_argument('-fp', '--filepath',
						help="Location of yelp reviews json data. Default: '/Users/kristiyan/Documents/MSiA 490 - Text Analytics/homework 3/yelp_data/yelp_academic_dataset_review.json'",
						default="/Users/kristiyan/Documents/MSiA 490 - Text Analytics/homework 3/yelp_data/yelp_academic_dataset_review.json", type=str)
	
	# Parse command line arguments
	args = parser.parse_args()
	logger.info(f'Successfully parsed command line arguments')

	# Accessing data and preprocessing in a parallel manner
	reviews, ratings = access_yelp_reviews(args.filepath)
	preprocessed_reviews = preprocess(reviews)

	number_words = 0
	number_characters = 0
	for review in preprocessed_reviews:
		for word in review:
			number_words += 1
			number_characters += len(word)

	logger.info(f"NUMBER OF WORDS/TOKENS: {number_words}")
	logger.info(f"NUMBER OF CHARACTERS: {number_characters}")
	logger.info(f"AVERAGE WORD LENGTH: {number_characters/number_words}")

	# Need the preprocessed_reviews as entire sentences, not lists of tokens
	preprocessed_reviews_strings = [" ".join(review) for review in preprocessed_reviews]

	# Saving preprocessed reviews with bigrams to pickle file
	with open('preprocessed_reviews_strings.pkl', 'wb') as f:
		pickle.dump(preprocessed_reviews_strings, f)

	with open('ratings.pkl', 'wb') as f:
		pickle.dump(ratings, f)
