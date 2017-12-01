"""
Created on Nov 14, 2017
@author: TYchoi

"""
import math
import numpy as np
import LSH
import pandas as pd

class CrossValidate(object):
    def __init__(self, input, output, n_folds=5):
        self.data_folds = {}
        self.n_folds = n_folds
        self.input = input
        self.output = output

    def split(self):
        nrows = self.input.shape[0]
        numbers = list(range(nrows))
        each_fold_size = math.floor(float(nrows)/self.n_folds)
        for i in range(1, self.n_folds):
            if i != self.n_folds:
                self.data_folds[i] = np.random.choice(numbers, each_fold_size, replace=False).tolist()
                for item in self.data_folds[i]:
                    numbers.remove(item)
        self.data_folds[self.n_folds] = numbers

    def evaluate_minhash(self, n, p):
        mean_accuracy = 0
        headers = []
        for i in range(1, self.n_folds + 1):
            headers.append("fold {}".format(i))
        headers.append("Mean")

        accuracy_list = []
        for i in range(1, self.n_folds+1):
            indices = self.data_folds[i]
            training = self.input.drop(self.input.index[indices])
            training_y = self.output.drop(self.output.index[indices])
            test = self.input.loc[self.input.index[indices], :]
            test_y = self.output.loc[self.output.index[indices], :]
            lsh = LSH.MinHash(training, training_y, n, p)
            lsh.train()
            lsh.predict(test, 5, 1)
            correct, counter, accuracy = lsh.accuracy(test_y)
            accuracy_list.append(accuracy)
            mean_accuracy += accuracy
        accuracy_list.append(float(mean_accuracy)/self.n_folds)
        accuracy_table = pd.DataFrame([accuracy_list], columns=headers)
        accuracy_table = accuracy_table.rename(index={0: "result"})
        print(accuracy_table)
        return accuracy_table
