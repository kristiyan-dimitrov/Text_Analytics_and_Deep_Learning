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
    

def dataset_stats(filepath):

	logger.info("Performin ls -l; Check for file size")
	subprocess.call(['ls','-l', filepath])
	logger.info("Performin wc -l; Check for review count")   
	subprocess.call(['wc','-l', filepath])

	reviews, ratings = access_yelp_reviews(filepath)  
	pd.Series(ratings).hist()
	plt.savefig('ratings_distribution.png')  # saves the current figure
	logger.info("Saved ratings histogram to ratings_distribution.png")


if __name__ == '__main__':
	# Setup CLI argument parser
	parser = argparse.ArgumentParser(description="Prints: line count and size of file to terminal; produces other truncated data statistics")
	parser.add_argument('-fp', '--filepath',
	                    help="Location of yelp reviews json data. Default: '/Users/kristiyan/Documents/MSiA 490 - Text Analytics/homework 3/yelp_data/yelp_academic_dataset_review.json'",
	                    default="/Users/kristiyan/Documents/MSiA 490 - Text Analytics/homework 3/yelp_data/yelp_academic_dataset_review.json", type=str)
	
	# Parse command line arguments
	args = parser.parse_args()
	logger.info(f'Successfully parsed command line arguments')

	dataset_stats(args.filepath)
