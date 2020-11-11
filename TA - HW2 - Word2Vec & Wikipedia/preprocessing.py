import os
import json
import gensim, logging
import argparse
import logging
import logging.config

from gensim import utils
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize


# Setup logging
logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.DEBUG)

logger = logging.getLogger(__file__)

def preprocess(json_file='enwiki-latest.json.gz', save_directory='data', number_files=50_000, verbose=1_000):

	test_iter = 1

	 # iterate over the plain text data we just created
	with utils.open(json_file, 'rb') as f:
	      
	    logger.info(f'Found {json_file} file and will process first {number_files} articles')  
	    
	    for line in f:

	        if test_iter  == number_files:
	            break
	        else:
	            if test_iter % verbose == 0:
	                logger.info(f'Finished processing {test_iter} files')
	            test_iter += 1
	        
	        # decode each JSON line into a Python dictionary object
	        article = json.loads(line)
	        
	        # If the given article ahs already been processed, skip it
	        if article['title']+'.txt' in os.listdir(save_directory):
	            continue
	        
	        article_sentences = list()
	        
	        for text in article['section_texts']:
	            # Split text into sentences
	            sentences = sent_tokenize(text)
	            # Preprocess each sentence converting it into a list of lower case tokens, which are not too long or too short
	            tokenized_sentences = [gensim.utils.simple_preprocess(sent) for sent in sentences]

	            # Remove any tokens which are stop words while preserving the sentence structure of the article (i.e. list of lists)
	            no_stops = list()
	            for tokenized_sentence in tokenized_sentences:
	                no_stops.append([word for word in tokenized_sentence if word not in stopwords.words('english')])
	            
	            # Add sentences from this article section to the list of all sentences for this article
	            article_sentences.extend(no_stops)
	            
	        # Save all sentences in this article to a txt file with the name of the article
	        try:
	            with open(os.path.join(save_directory, article['title']+'.txt'), 'w') as filehandle:
	                for listitem in article_sentences:
	                    filehandle.write(f'{" ".join(listitem)}\n')
	        	logger.info(f'Successfully saved {article['title']+'.txt'} to {save_directory}')
	        except:
	            logger.error(f"FAILED TO SAVE {article['title']}")


if __name__ == '__main__':
	# Setup CLI argument parser
	parser = argparse.ArgumentParser(description="Preprocess Wikipedia articles from JSON dump file and save each processed article as a .txt file")
	parser.add_argument('-f', '--filename',
	                    help="Filename of JSON dump file with Wikipedia articles. Default: 'enwiki-latest.json.gz'",
	                    default="enwiki-latest.json.gz", type=str)
	parser.add_argument('-d', '--directory',
	                    help="Directory where to save processed articles as .txt files; Default: ./data/",
	                    default="data", type=str)
	parser.add_argument('-n', '--number_files',
	                    help="Number of files (articles) to preprocess and save as .txt files. Default: 50000",
	                    default=50000, type=int)
	parser.add_argument('-v', '--verbose',
	                    help="How often to print number of files processed i.e. once every X articles. Default: 1000",
	                    default=1000, type=int)
	
	# Parse command line arguments
	args = parser.parse_args()
	logger.info(f'Successfully parsed command line arguments')

	preprocess(args.filename, args.directory, args.number_files, args.verbose)
