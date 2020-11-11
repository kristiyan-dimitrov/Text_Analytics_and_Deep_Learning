# Homework 1 - Kristiyan Dimitrov

## Problem 1 Instructions

To run my solution:
- Clone the repo
- Cd into the repo
- Then do: 
```bash
python problem1.py
```
Expected results:
- the code will run for ~20 seconds
- there should be 4 log messages indicating success along different parts of the script
- you should see a file called processed_text.pkl
- this is a serialized Doc object from the SpaCy package. It contains tokens with POS tags and other attributes for the book "Crime and Punishment".
- file size ~150 MB.
- see Jupyter notebook for details

## Problem 2 - Part 1 Instructions

Assuming you've already cloned the repo, do:
- Download and unzip text corpus file in the root of the repo: http://qwone.com/~jason/20Newsgroups/20news-bydate.tar.gz
- You should see a folder `20_newsgroups`

```bash
python problem2_part1.py
```
Expected behavior:
- The script will run for ~20 seconds and you will see a lot of log messages.
- In each subfolder of 20_newsgroups you will see an `emails.txt` file, which contains all the emails parsed from the files in that subfolder.

## Problem 2 - Part 2 Instructions

Assuming you've already cloned the repo, as well as downloaded and unzipped the 20_newsgroups corpus as described above:
- From the root of the repo run:
```bash
python problem2_part2.py
```
Expected Behavior:
- Similar to part1, you should see dates.txt in each subfolder of 20_newsgroups.
