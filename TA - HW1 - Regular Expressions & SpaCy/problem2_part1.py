import re
import io
import os
import argparse
import logging
import logging.config

# Setup logging
logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
						datefmt='%m/%d/%Y %I:%M:%S %p',
						level=logging.DEBUG)

logger = logging.getLogger(__file__)

def find_emails(filepath):
	'''
	Recursively walks down the directory tree starting at provided filepath.
	For each folder, writes an emails.txt with all emails found in files in that folder.

	Args:
		filepath (str): string representing filepath for root directory from which to begin extracting email addresses.
	Return:
		None; Saves emails to emails.txt in each folder
	'''

	for root, subdirs, files in os.walk(filepath):
		list_file_path = os.path.join(root, 'emails.txt')

		with open(list_file_path, 'w') as list_file:

			for filename in files:
				file_path = os.path.join(root, filename)

				with io.open(file_path, 'r', encoding='windows-1252') as f:
					try:
						f_content = f.read()
						pattern = r'[a-zA-Z0-9_\.\#\!\?]+@\w+\.\w+'
						emails = re.findall(pattern, f_content)
						for email in emails:
							list_file.write(email)
							list_file.write('\n')

						logger.info(f'Found {len(emails)} emails in {file_path}')
					except:
						continue

		logger.info(f'Successfully traversed all files in {list_file_path} and saved emails to emails.txt')
		

if __name__ == '__main__':
	
	# Setup CLI argument parser
	parser = argparse.ArgumentParser(description="Recursively walks down the directory tree starting at provided filepath. For each folder, writes an emails.txt with all emails found in files in that folder.")
	parser.add_argument('-fp', '--filepath',
						help="Filepath as root of directory tree. Default: 20_newsgroups",
						default="20_newsgroups", type=str)
	# Parse command line arguments
	args = parser.parse_args()
	logger.info(f'Successfully parsed command line arguments')

	find_emails(args.filepath)