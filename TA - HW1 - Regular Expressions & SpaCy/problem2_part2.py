import re
import os
import io
import argparse
import logging
import logging.config

# Setup logging
logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.DEBUG)

logger = logging.getLogger(__file__)

def find_dates(filepath):
	'''
	Finds all dates in file at specified filepath.

	Args:
		filepath (str): string representing filepath of text to be searched for dates.
	Return:
		None; Saves dates to dates.txt

	'''
	for root, subdirs, files in os.walk(filepath):
		list_file_path = os.path.join(root, 'dates.txt')

		with open(list_file_path, 'w') as list_file:

			for filename in files:
				file_path = os.path.join(root, filename)

				try:
					with io.open(file_path, 'r') as f:
						text = f.read()

						pattern1 = r'\d{1,2}/\d{1,2}/\d{4}'
						dates1 = re.findall(pattern1, text)

						pattern2 = r'\w+\s\d{2}\w{2}\s\d{4}'
						dates2 = re.findall(pattern2, text)

						pattern3 = r'\d{2}\.\d{2}\.\d{4}'
						dates3 = re.findall(pattern3, text)

						pattern4 = r'\d{1,2}\s[JFMASOND]\w{2}\s\d{4}'
						dates4 = re.findall(pattern4, text)
						
						dates = dates1+dates2+dates3+dates4
						

						for date in dates:
							list_file.write(date)
							list_file.write('\n')

						logger.info(f'Found {len(dates)} dates in {file_path}')

				except:
					logger.info(f'Failed to decode file {file_path}')
					continue

		logger.info(f'Successfully traversed all files in {list_file_path} and saved dates to dates.txt')


if __name__ == '__main__':
	
	# Setup CLI argument parser
	parser = argparse.ArgumentParser(description="Recursively walks down the directory tree starting at provided filepath. For each folder, writes an dates.txt with all emails found in files in that folder.")
	parser.add_argument('-fp', '--filepath',
	                    help="Filepath for text file. Default: text.txt",
	                    default="20_newsgroups", type=str)
	# Parse command line arguments
	args = parser.parse_args()
	logger.info(f'Successfully parsed command line arguments')

	find_dates(args.filepath)