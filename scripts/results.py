import pandas
from sklearn.metrics import accuracy_score, precision_score, recall_score, cohen_kappa_score
import numpy as np
import numpy
import tabulate

#feature selection

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import f_classif


class Results:

	def __init__(self, size):
		self.lastPos = 0
		self.accuracies = numpy.zeros(size)
		self.precisions = numpy.zeros(size)
		self.recalls = numpy.zeros(size)
		self.kappas = numpy.zeros(size)
		self.ttest = numpy.zeros(size)

	def addResult(self, accuracy,precision,recalls,kappas):

		self.accuracies[self.lastPos] = accuracy
		self.precisions[self.lastPos] = precision
		self.recalls[self.lastPos] = recalls
		self.kappas[self.lastPos] = kappas
		

		self.lastPos+=1

	def printStatistics(self):


		accuracy_mean = numpy.mean(self.accuracies)
		precision_mean = numpy.mean(self.precisions)
		recalls_mean = numpy.mean(self.recalls)
		kappas_mean = numpy.mean(self.kappas)
		mean_array = np.array(['mean',accuracy_mean,precision_mean,recalls_mean,kappas_mean])

		accuracy_std = numpy.std(self.accuracies)
		precision_std = numpy.std(self.precisions)
		recalls_std = numpy.std(self.recalls)
		kappas_std = numpy.std(self.kappas)
		std_array = np.array(['standard dev',accuracy_std,precision_std,recalls_std,kappas_std])

		accuracy_last = self.accuracies[self.lastPos-1]
		precision_last = self.precisions[self.lastPos-1]
		recall_last = self.recalls[self.lastPos-1]
		kappas_last = self.kappas[self.lastPos-1]
		last_array = np.array(['last val',accuracy_last,precision_last,recall_last,kappas_last])

		accuracy_maxValue = numpy.amax(self.accuracies)
		precision_maxValue = numpy.amax(self.precisions)
		recall_maxValue = numpy.amax(self.recalls)
		kappas_maxValue = numpy.amax(self.kappas)
		maxValue_array = np.array(['max val',accuracy_maxValue,precision_maxValue,recall_maxValue,kappas_maxValue])

		accuracy_minValue = numpy.amin(self.accuracies)
		precision_minValue = numpy.amin(self.precisions)
		recall_minValue = numpy.amin(self.recalls)
		kappas_minValue = numpy.amin(self.kappas)
		minValue_array = np.array(['min val',accuracy_minValue,precision_minValue,recall_minValue,kappas_minValue])

		head = np.array(['accuracy','precision','recall','kappa'])		
		table = np.array([mean_array,std_array,last_array,minValue_array, maxValue_array])

		print tabulate.tabulate(table,headers=head)