import argparse
import logging
import logging.config
import pickle
import spacy

from urllib import request

# Setup logging
logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.DEBUG)

logger = logging.getLogger(__file__)

def spacy_tagger(filepath):
	'''
	This function does the following in this order:
	- downloads the book Crime and Punishment from the Gutenberg project
	- loads the small Spacy language model
	- performs tokenization, lemmatization, and part of speech tagging on the text
	- saves spacy doc object to processed_text.pkl
	'''
	url = "http://www.gutenberg.org/files/2554/2554-0.txt"
	response = request.urlopen(url)
	raw = response.read().decode('utf8')

	logger.info(f'Successfully downloaded and loaded Crime & Punishment from "http://www.gutenberg.org/files/2554/2554-0.txt".')

	nlp = spacy.load("en_core_web_sm") # small english model
	nlp.disable_pipes('parser', 'ner')
	nlp.max_length = 1_500_000 # increasing maximum number of characters
	doc = nlp(raw)

	logger.info(f'Successfully processed text with SpaCy en_core_web_sm')	

	with open(filepath, 'wb') as filehandle:
		pickle.dump(doc, filehandle)

	logger.info(f'Successfully saved processed text to {filepath}')

if __name__ == '__main__':
	
	# Setup CLI argument parser
	parser = argparse.ArgumentParser(description='Downloads "Crime and Punishment" from the Gutenberg project and applies tokenization, lemmatization, and POS tagging. Saves result to processed_text.pkl')
	parser.add_argument('-fp', '--filepath',
	                    help="Filepath to save file. Default: processed_text.pkl",
	                    default="processed_text.pkl", type=str)
	# Parse command line arguments
	args = parser.parse_args()
	logger.info(f'Successfully parsed command line arguments')

	spacy_tagger(args.filepath)
