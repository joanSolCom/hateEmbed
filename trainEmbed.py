import os, sys
import gensim, logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class MySentences(object):

	def __init__(self, dirname, low):
		self.dirname = dirname
		self.low = low

	def __iter__(self):
		for fname in os.listdir(self.dirname):
			for line in open(os.path.join(self.dirname, fname)):
				if len(line.split()) >= 2:
					if "nolow" in self.low : yield line.replace("\n","").split(" ")
					else: yield line.lower().replace("\n","").split(" ")


#-------------------------
size=[300]
window=[6]
min_count=[10]

dataPath =  sys.argv[1]
modelPath = sys.argv[2] + "model_swm_"
low = sys.argv[3]

sentences = MySentences(dataPath, low)

for s in size:
	for w in window:
		for m in min_count:
			filename = modelPath + str(s) +"-"+ str(w) +"-"+ str(m) + "-" + low		
			print "Processing " + filename
			model = gensim.models.Word2Vec(sentences, size=s, window=w, min_count=m)
			model.save(filename)
			model.save_word2vec_format(filename+".w2v")
			
print "Stai senza pensieri."