from gensim import models
from sklearn.pipeline import Pipeline
from sklearn.ensemble import ExtraTreesClassifier
import numpy as np
from sklearn.svm import SVC
import os
from sklearn.cross_validation import cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from collections import defaultdict

class Embedding:

	def __init__(self, modelPath):
		#self.model = models.KeyedVectors.load_word2vec_format('/home/joan/Escritorio/trainEmbed/genericw2v/GoogleNews-vectors-negative300.bin', binary=True) 
		self.model = models.Word2Vec.load(modelPath)
		self.w2v = dict(zip(self.model.wv.index2word, self.model.wv.syn0))
		self.dim = len(self.w2v.itervalues().next())

	def getWordVector(self, word):
		vector = np.zeros(self.dim)
		if word in self.w2v:
			vector = self.w2v[word]
		return vector

	def getW2V(self):
		return self.w2v

	def computeSimilarity(self, word1, word2):
		return self.model.similarity(word1, word2)

	def getAvgVectors(self, directory):
		avgVectors = []
		labels = set()
		for fname in os.listdir(directory):
			label = fname.split("_")[2]
			labels.add(label)
			fd = open(directory+fname,"rb")
			words = fd.read().lower().split()
			vectors = []
			for word in words:
				vector = self.getWordVector(word)
				vectors.append(vector)

			avgVector = np.mean(vectors,axis=0)
			avgVectors.append((avgVector,label))
			fd.close()

		return avgVectors, labels

	def toArff(self, path, fname, avgVectors, labels):
		fd = open(path+fname,"w")
		arffString = "@relation "+ fname+ "\n"

		nFeats = len(avgVectors[0][0])

		for i in range(0,nFeats):
			arffString += '@attribute dim'+str(i)+' numeric\n'

		labelString = "@attribute label {"
		for label in labels:
			labelString+=label+","

		labelString = labelString[:-1]

		labelString+="}\n"
		arffString += labelString
		arffString += "\n@data\n"

		for instance in avgVectors:
			featVector = instance[0]
			featVector = map(str, featVector)    
			arffString += ",".join(featVector)
			arffString += "," + instance[1] + "\n"

		fd.write(arffString.encode("utf-8"))
		fd.close()

'''
if __name__ == '__main__':

	embedPath = "/home/joan/Escritorio/trainEmbed/w2v/model_swm__stormfrontNEW_200_5_10_low"
	outPath = "/home/joan/Escritorio/trainEmbed/outputs/"
	fname = "model_swm__stormfrontNEW_200_5_10_low.arff"
	pathTest = "/home/joan/Escritorio/Datasets/hateSpeech/meuCorpusHate/clean/"
	
	iHate = Embedding(embedPath)
	avgVectors, labels = iHate.getAvgVectors(pathTest)
	iHate.toArff(outPath, fname, avgVectors, labels)
'''

class MeanEmbeddingVectorizer(object):
    def __init__(self, word2vec):
        self.word2vec = word2vec
        # if a text is empty we should return a vector of zeros
        # with the same dimensionality as all the other vectors
        self.dim = len(word2vec.itervalues().next())

    def fit(self, X, y):
        return self

    def transform(self, X):
        return np.array([
            np.mean([self.word2vec[w] for w in words if w in self.word2vec]
                    or [np.zeros(self.dim)], axis=0)
            for words in X
        ])

class TfidfEmbeddingVectorizer(object):
    def __init__(self, word2vec):
        self.word2vec = word2vec
        self.word2weight = None
        self.dim = len(word2vec.itervalues().next())

    def fit(self, X, y):
        tfidf = TfidfVectorizer(analyzer=lambda x: x)
        tfidf.fit(X)
        # if a word was never seen - it must be at least as infrequent
        # as any of the known words - so the default idf is the max of 
        # known idf's
        max_idf = max(tfidf.idf_)
        self.word2weight = defaultdict(
            lambda: max_idf,
            [(w, tfidf.idf_[i]) for w, i in tfidf.vocabulary_.items()])

        return self

    def transform(self, X):
        return np.array([
                np.mean([self.word2vec[w] * self.word2weight[w]
                         for w in words if w in self.word2vec] or
                        [np.zeros(self.dim)], axis=0)
                for words in X
            ])

	


if __name__ == '__main__':

	embedPath = "/home/joan/Escritorio/trainEmbed/w2v/model_swm__returnofkings_rooshv_400_7_5_low"
	iHate = Embedding(embedPath)
	w2v = iHate.getW2V()

	etree_w2v = Pipeline([("word2vec vectorizer", MeanEmbeddingVectorizer(w2v)), ("extra trees", ExtraTreesClassifier(n_estimators=200))])
	etree_w2v_tfidf = Pipeline([("word2vec vectorizer", TfidfEmbeddingVectorizer(w2v)),("extra trees", ExtraTreesClassifier(n_estimators=200))])
	svm_w2v = Pipeline([("word2vec vectorizer", MeanEmbeddingVectorizer(w2v)), ("SVM", SVC(C=1.0, kernel="rbf", degree=3, gamma='auto', coef0=0.0, shrinking=True, tol=0.001, cache_size=200, class_weight=None, verbose=False))])
	svm_w2v_tfidf = Pipeline([("word2vec vectorizer", TfidfEmbeddingVectorizer(w2v)),("SVM", SVC(C=1.0, kernel="rbf", degree=3, gamma='auto', coef0=0.0, shrinking=True, tol=0.001, cache_size=200, class_weight=None, verbose=False))])
	randFor_w2v = Pipeline([("word2vec vectorizer", MeanEmbeddingVectorizer(w2v)), ("Rand For", RandomForestClassifier(n_estimators=10, criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=None, min_impurity_split=1e-07, bootstrap=True, oob_score=False, n_jobs=-1, random_state=None, verbose=0, warm_start=False, class_weight=None))])
	randFor_w2v_tfidf = Pipeline([("word2vec vectorizer", TfidfEmbeddingVectorizer(w2v)),("Rand For", RandomForestClassifier(n_estimators=10, criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=None, min_impurity_split=1e-07, bootstrap=True, oob_score=False, n_jobs=-1, random_state=None, verbose=0, warm_start=False, class_weight=None))])

	all_models = [("randFor_w2v",randFor_w2v),("randFor_w2v_tfidf",randFor_w2v_tfidf),("etree_w2v", etree_w2v),("etree_w2v_tfidf", etree_w2v_tfidf),("svm_w2v",svm_w2v),("svm_w2v_tfidf", svm_w2v_tfidf)]
	pathTest = "/home/joan/Escritorio/Datasets/hateSpeech/meuCorpusHate/clean/"


	X, y = [], []

	for fname in os.listdir(pathTest):
		fd = open(pathTest+fname,"r")
		text = fd.read()
		label  = fname.split("_")[2]
		X.append(text.split())
		y.append(label)
		fd.close()


	X, y = np.array(X), np.array(y)
	print "total examples %s" % len(y)

	for name, model in all_models:
		print name, cross_val_score(model, X, y, cv=10).mean()
