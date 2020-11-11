import os
import json
import gensim, logging
import argparse
import logging
import logging.config

from gensim import utils

# Setup logging
logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.DEBUG)

logger = logging.getLogger(__file__)

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname
 
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            if fname in ['.ipynb_checkpoints', '.DS_Store']:
                continue
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()

def train_model(directory='data', name='word2vec.model', **kwargs):
	'''
	Trains word2vec model on all files in specified directory and saves trained model
	Args:
		directory (str): Directory where to look for processed articles as .txt files
		name (str): 
		**kwargs: additional keyword arguments to modify the defaults for gensim.models.Word2Vec; for example size, window, sg, hs, min_count, etc.
		Check documentation for options: https://radimrehurek.com/gensim/models/word2vec.html

	Returns:
		VOID: saves model to .model object
	'''

	sentences = MySentences(directory) # a memory-friendly iterator

	model = gensim.models.Word2Vec(sentences, **kwargs)

	model.save("word2vec.model")

if __name__ == '__main__':
	# Setup CLI argument parser
	parser = argparse.ArgumentParser(description="Trains word2vec model on all files in specified directory and saves trained model")
	parser.add_argument('-d', '--directory',
	                    help="Directory where to look for processed articles as .txt files; Default: ./data/",
	                    default="data", type=str)
	parser.add_argument('-n', '--name',
                    help="Filename for saved model object. Default: 'word2vec.model'",
                    default="word2vec.model", type=str)

	
	# Parse command line arguments
	args = parser.parse_args()
	logger.info(f'Successfully parsed command line arguments')

	train_model(args.directory, args.name)