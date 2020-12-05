import os
import pickle
import logging
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

MODEL_FILE = os.environ.get('MODEL_FILE')
logger.info(f"Fetched environment variable MODEL_FILE: {MODEL_FILE}")
CATEGORIES_FILE = os.environ.get('CATEGORIES_FILE')
logger.info(f"Fetched environment variable CATEGORIES_FILE: {CATEGORIES_FILE}")

with open(MODEL_FILE, 'rb') as handle:
    model = pickle.load(handle)
    logger.info(f"Successfully loaded model from {MODEL_FILE}")

with open(CATEGORIES_FILE, 'rb') as handle:
    categories = pickle.load(handle)
    logger.info(f"Successfully loaded categories from {CATEGORIES_FILE}")
# print(" -------- CATEGORIES just loaded in predict.py: ", categories)

def predict(description):
    '''Makes a one-hot prediction and decodes that into actual categories'''

    one_hot_prediction = model.predict(description)
    one_indices = np.where(one_hot_prediction==1)[1]
    category_predictions = categories[one_indices]

    return category_predictions