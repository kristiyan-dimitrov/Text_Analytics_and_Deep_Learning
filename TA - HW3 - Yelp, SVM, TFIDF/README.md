# kristiyan-dimitrov_msia_text_analytics_2020

This repo contains code for generating a Logistic Regression or SVM classifier for Yelp reviews.

Here's what you need to do to recreate:

## 1. Get the data

Go to [this link](https://www.yelp.com/dataset/download) and download the data.
After you download it, unzip it. You will be working with the reviews json file.

## 2. Look at some dataset stats
```bash
python dataset_stats.py -fp=<filepath to the reviews.json file>
```

## 3. Preprocess the first 500,000 reviews
```bash
python preprocess -fp=<filepath to the reviews.json file>
```
This step will take ~25 minutes.
The result will be a pickle file with the tokenized and cleaned review texts as well as a separate file with the ratings.

## 4. Generate corpuses
```bash
python generate_corpuses.py
```
This will produce 4 corpus files (BOW & TFIDF, unigram & uni+bigram).
It will also produce the tfidf_vectorizer used for the last corpus - the TFIDF uni+bigram.
This will be used for predictive purposes since it performs best. Of course, you can use the other ones if you want.

## 5. Train model
```bash
python train_model.py -m=SVM
```
This will train an SVM model on all 500,000 yelp reviews from the uni_and_bigram_tfidf_corpus.
It will also save the trained model object to a pickle file.

## 6. Use the model for predictions
```bash
python predict_svm.py -f=texts.txt
```
I've included a dummy file with 3 reviews I just made up in texts.txt.
The script will use the tfidf_vectorizer to prepare all the dummy reviews in texts.txt.
Then it will load the trained model object and make a rating prediction for each review.
These predictions will be saved to result.json file in the form {'label_X':<predicted_rating on a scale from 1 to 5>} 
where X is from 1 to number of reviews in texts.txt

Examples:
- This Italian restaurant really sucks. The salad was terrible. --> Predicted rating is: 1
- I really loved my time at this bakery. The bread was fluffy and tasty. Will definitely come back for more. --> Predicted rating is: 5
- What did I think of this restaurant? I'm not really sure. --> Predicted rating is: 4
