import  os, re
import math, random

import sklearn
X, Y = [], []
testSet = []
def main():
	arff = open("essays.arff", "w")


	feature_functions = [length, avg_word_length, avg_sentence_length, avg_long_words, num_yous, percent_distinct_words]    
									  #to add more features, just define

									  #the functions and add to this list
	arff.write("@RELATION essay\n")
	for feature in feature_functions:

		arff.write("@ATTRIBUTE " +\

					str(feature.__name__) + " REAL\n")  #change this if we

													 #have non-real number

													 #values

	###PREDEFINED USER FEATURES#######
	arff.write("@ATTRIBUTE score {"+','.join([str(x) for x in range(61)])+"}\n")  

	arff.write("@DATA\n")

	training_file = open('training.tsv')

	firstLine = True
	for line in training_file: 
		if not firstLine:
			if random.randint(0,10) == 4:
				testSet.append(line)
			else:
				extract_features(feature_functions, line, arff)
		else:
			firstLine = False


	#build a model
	from sklearn import tree
	clf = tree.DecisionTreeClassifier()
	clf = clf.fit(X, Y)

	yes, no = 0.0, 0.0
	for line in testSet:
		a = activate(feature_functions, line, clf)

		if a:
			yes += 1
		else:
			no += 1

	print "Accuracy: " + str(yes/(yes+no))


def avg_word_length(essay):
	essay = essay.split(" ")
	return average([len(x) for x in essay])

def avg_sentence_length(essay):
	return average([len(x.split(" ")) for x in essay.split('.')])

def num_yous(essay):
	return len([x for x in essay.split() if 'you' in x])

def percent_distinct_words(essay):
	return float(len(set([x.lower() for x in essay.split()]))) / len([x.lower() for x in essay.split()])

def avg_long_words(essay):
	return float(len([x.lower for x in essay.split if x.len > 5]) / len([x.lower for x in essay.split()]))

def average(l):
	s, s1 = 0,0.0
	for x in l:
		s1 += 1
		s += int(x)
	return s/s1
def activate(feature_funcitons, line, classifier):
	line = line.split('\t')
	typee = line[1]
	essay = line[2]
	if typee == '1':
		r = 12
		score = line[6] #0-6
	elif typee == '2':
		r = 20
		score = str(int(line[6]) + int(line[7]) + int(line[8]) + int(line[9])) #0-4,0-6,0-4,0,6
	elif typee == '3' or typee == '4':
		r = 3
		score = line[6] #0-3
	elif typee == '5' or typee == '6': #0-4
		r = 4
		score = line[6] 
	elif typee == '7': #0-30
		r = 30
		score = line[6] 
	elif typee == '8': #0-60
		r = 60
		score = line[6]
	r = float(r)

	normalScore = int((int(score) / r) * 100)
	buff = ""
	values = []
	for feature in feature_funcitons:

		value = feature(essay)


		values.append(value)

	classifiedScore = float(classifier.predict([int(x) for x in values]))

	# classifiedScore = (classifiedScore/100)*r
	classifiedScore /= (100/r)
	classifiedScore = round(classifiedScore, 0)

	score = int(score)
	scores = [score]
	return int(classifiedScore) in scores


def extract_features(feature_funcitons, line, arff):
	line = line.split('\t')
	typee = line[1]
	essay = line[2]
	if typee == '1':
		r = 12
		score = line[6] #0-6
	elif typee == '2':
		r = 20
		score = str(int(line[6]) + int(line[7]) + int(line[8]) + int(line[9])) #0-4,0-6,0-4,0,6
	elif typee == '3' or typee == '4':
		r = 3
		score = line[6] #0-3
	elif typee == '5' or typee == '6': #0-4
		r = 4
		score = line[6] 
	elif typee == '7': #0-30
		r = 30
		score = line[6] 
	elif typee == '8': #0-60
		r = 60
		score = line[6]
	r = float(r)
	if typee != '4':
		return 
	normalScore = int((int(score) / r) * 100)
	buff = ""
	values = []
	for feature in feature_funcitons:

		value = feature(essay)


		values.append(value)
	buff += (",".join([str(x) for x in values]) + "," + str(score) + "\n")
	values = [int(x) for x in values]
	X.append(values)
	Y.append(normalScore)
	if typee == '4':
		arff.write(buff)

def length(essay):
	return len(essay.split(" "))


if __name__ == "__main__":
	main()
