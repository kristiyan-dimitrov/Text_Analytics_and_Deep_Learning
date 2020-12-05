import os
import pickle
import logging
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

TFIDF_VECTORIZER_FILE = os.environ.get('TFIDF_VECTORIZER_FILE')
logger.info(f"Fetched environment variable TFIDF_VECTORIZER_FILE: {TFIDF_VECTORIZER_FILE}")


def preprocess(description):
    '''Tokenizes, removes stopwords, and returns reconstructed string'''
    tokenized_description = simple_preprocess(description[0])
    logger.info("Tokenized description")

    no_stops = [word for word in tokenized_description if word not in stopwords.words('english')]
    logger.info("Removed stopwords")

    clean_description = " ".join(no_stops)
    logger.info("Reconstructed description")

    with open(TFIDF_VECTORIZER_FILE, 'rb') as handle:
        tfidf_vectorizer = pickle.load(handle)
        logger.info(f"Successfully loaded tfidf_vectorizer from {TFIDF_VECTORIZER_FILE}")

    transformed_description = tfidf_vectorizer.transform([clean_description])
    logger.info("Converted to TF-IDF")

    return transformed_description
