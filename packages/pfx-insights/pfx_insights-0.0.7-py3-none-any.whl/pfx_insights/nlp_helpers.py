import os
import string
import nltk
from nltk.stem.wordnet import WordNetLemmatizer

class NlpProcessor:
	def __init__(self,
              pos_tags_to_ignore = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'JJ', 'JJR', 'JJS', 'CD']
              ):
		self.exclude_chars = [i for i in set(string.punctuation) if i not in ['.']]
		self.pos_tags_to_ignore = lambda pos: pos in pos_tags_to_ignore

		self.lemmatizer = WordNetLemmatizer()
		self.stop_words   = set(nltk.corpus.stopwords.words('english'))
		self.stop_words = [self.lemmatizer.lemmatize(word) for word in self.stop_words]
		self.numericals = [str(i) for i in range(0,3000)]

		current_folder = os.path.dirname(os.path.abspath(__file__))
		bing_stopwords_file = os.path.join(current_folder, 'resources/bing_stopwords.txt')

		self.bing_stopwords = []
		with open(bing_stopwords_file, 'r') as f:
			for stop_word in f:
				self.bing_stopwords.append(stop_word)		

	def clean_doc(self, doc, min_length = 3):
		doc = str(doc)
		doc = ''.join([ch for ch in doc if ch not in self.exclude_chars])

		tokens = nltk.word_tokenize(doc)
		tagged = nltk.pos_tag(tokens)
		filtered_pos = ' '.join([word for (word, pos) in tagged if not self.pos_tags_to_ignore(pos)]) # not verbs, adjectives or constants	

		normalized = [self.lemmatizer.lemmatize(word) for word in filtered_pos.lower().split()]

		stop_free = [i for i in normalized if i not in self.stop_words]
		bing_stop_free = [i for i in stop_free if i not in self.bing_stopwords]
		numericals_free = [i for i in bing_stop_free if i not in self.numericals]
		len_ge_min = " ".join([i for i in numericals_free if len(i) >= min_length])

		return len_ge_min