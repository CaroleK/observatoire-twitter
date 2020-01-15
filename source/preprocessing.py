#sentence segmentation
#normalization and tokenization
#POS tagging# named entity recognition
import pandas as pd
import sys
sys.path.insert(0, "D:/Centrale 3A/OSY/Data Science/repos/observatoire-twitter")

class Preprocess:
     def __init__(self, file, full_df=None, text_df=None):
        self.file = file
        self.full_df = full_df
        self.text_df = text_df
     
     def convert_to_df(self, nrows=None):
         full_df = pd.read_csv(self.file, nrows= nrows)
         self.full_df = full_df
         
         text_df = full_df[["text"]].copy()
         text_df["raw"] = text_df["text"].astype(str)
         self.text_df = text_df

     def remove_upper_cases(self, text):
        return text.lower()
    
     def remove_punctuation(self, text):
         """custom function to remove the punctuation"""
         import string
         PUNCT_TO_REMOVE = string.punctuation
         return text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))
     
     def remove_stopwords(self, text):
         """custom function to remove the stopwords"""
         import nltk
         nltk.download('stopwords')
         link_downloaded = "C:\\Users\\carol\\AppData\\Roaming\\nltk_data\\corpora\\stopwords"
         STOPWORDS = set(open(link_downloaded).read().split())
         return " ".join([word for word in str(text).split() if word not in STOPWORDS])

     def remove_frequent_words(self, text):
        from collections import Counter
        cnt = Counter()
        for text in self.text_df["text_wo_stop"].values:
            for word in text.split():
                cnt[word] += 1
     
     def process_text (self, lower_cases = False, remove_punctuation = False, remove_stopwords = False, remove_frequent_words = False):
         if lower_cases:
             self.text_df["processed"] = self.text_df["raw"].apply(lambda t: self.remove_upper_cases(t))
         if remove_punctuation:
             self.text_df["processed"] = self.text_df["processed"].apply(lambda t: remove_punctuation(t))
         if remove_stopwords:
             self.text_df["processed"] = self.text_df["processed"].apply(lambda t: remove_stopwords(t))
        