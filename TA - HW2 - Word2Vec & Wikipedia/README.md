# kristiyan-dimitrov_msia_text_analytics_2020

IMPORTANT:
- The data I've included is just a sample of 77 articles;
- In reality I had 55,170 articles, which would have been too much to upload to GitHub
- You can recreate my work using the steps below, but I don't advise it, because it will take >10 hours.
- Instead, look over the scripts then check the _bottom_ of Homework2_NOTEBOOK.pdf for some exploration of how the model performs.

Steps to recreate:

- Use [this link](https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2) to download ~18GB of XML data dump with the latest version of the English Wikipedia: 
- Then run the following command to extract a JSON file from the XML data dump:
```bash
python -m gensim.scripts.segment_wiki -m 1000 -f enwiki-latest-pages-articles.xml.bz2 -o enwiki-latest.json.gz
```

Note: the number 1000 refers to a number of characters threshold. Any articles with fewer characters will be discarded.

- run preprocessing.py
```bash
python preprocessing.py
```
Note: Expected time to completion: ~8 hours for 50,000 articles on my MacBook Pro.

- run model_training.py
```bash
python model_training.py
```
Note: Expected time to completion: ~5-10 minutes depending on parameters you give the model.
