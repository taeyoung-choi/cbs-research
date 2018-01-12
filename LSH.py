"""
Created on Oct 24, 2017
@author: TYchoi

"""

import random
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup

class MinHash(object):
    """
    Locality Sensitive Hashing using Minhash and recommends items using approximate nearest neighbors.

    Attributes:
        input               input matrix for training
        output              output matrix for validating
        hash_size           number of hash functions within each band
        band_size           number of bands
        row_num             number of rows of the input matrix
        col_num             number of columns of the input matrix
        hash_function       list of random hash functions of size hash_size * band_size
        signature_matrix    matrix that contains the minimum values of hashed indicies that user has consumed
        neighbors           list of users that shares the same hash value
        items               dictionary of items {number: item}. This serves as keys that we want to hash
        headers             list of category names
        result              dataframe that stores neighbors and recommended items for each user
    """
    def __init__(self, input_matrix, output_matrix, hash_size, band_size):
        self.input = input_matrix
        self.output = output_matrix
        self.hash_size = hash_size
        self.band_size = band_size
        self.hash_function = []
        self.signature_matrix = pd.DataFrame(columns=list(range(band_size)))
        self.neighbors = []
        self.user_num = self.input.shape[0]
        self.items = {}
        self.headers = list(input_matrix)
        self.result = pd.DataFrame(columns=['neighbors', 'item'])
        self.program_by_category = {}
        self.program_by_date = {}

        # unique items are keys we want to hash
        counter = 0
        for header in self.headers:
            for item in set(input_matrix[header].tolist()):
                # some items have the same names for different columns
                self.items[header+item] = counter
                counter += 1
        self.item_num = len(self.items)
        self.program_category_mapper()

    def program_category_mapper(self):
        with urllib.request.urlopen("https://www8.gsb.columbia.edu/execed/program-finder") as response:
            html = response.read()
            soup = BeautifulSoup(html, 'lxml')
            table = soup.find('table', {'class': 'views-table cols-17'})
            courses = table.find_all('div', {'class': 'heading'})
            topics = table.find_all('div', {'class': 'pf_col span_2_of_12 span_1_of_6 span_3_of_4 '})
            dates = table.find_all('div', {'class': 'pf_col span_3_of_12 span_1_of_6 span_3_of_4 pf_paddingBelowShowMore '})
            for i in range(len(courses)):
                program_name = courses[i].text.replace('NEW', '').strip()
                self.program_by_category[program_name] = topics[i].text.strip()
                self.program_by_date[program_name] = dates[i].text.strip()

    def train(self):
        self.create_hash_functions()
        self.to_signature_matrix()
        self.neighboring()

    def predict(self, data, n, p):
        for i in range(data.shape[0]):
            user = data.iloc[i, :]
            neighbors, classes = self.find_neighbors(user)
            courses = self.recommend_courses(classes, n, p)
            self.result.loc[i] = [neighbors, courses]

    def accuracy(self, y):
        counter = 0
        correct = 0
        for i in range(y.shape[0]):
            if y.iloc[i]['Program Name'] in self.result.iloc[i]['item']:
                correct += 1
                counter += 1
            else:
                counter += 1
        return correct, counter, float(correct) / counter

    def create_hash_functions(self):
        function_list = []
        # p is a prime number that is greater than max possible value of x
        found = False
        p = self.item_num
        while not found:
            prime = True
            for i in range(2, p):
                if p % i == 0:
                    prime = False
            if prime:
                found = True
            else:
                p += 1
        # Corman et al as very readable information in section 11.3.3 pp 265-268.
        # https://mitpress.mit.edu/books/introduction-algorithms
        for i in range(self.band_size):
            for j in range(self.hash_size):
                # a is any odd number you can choose between 1 to p-1 inclusive.
                a = random.randrange(1, p, 2)
                # b is any number you can choose between 0 to p-1 inclusive.
                b = random.randint(0, p)
                function_list.append([a, b, p])
        self.hash_function = function_list

    def to_signature_matrix(self):
        sig_mat = []
        for i in range(self.user_num):
            user = self.input.iloc[i, :]
            each = []
            for func in self.hash_function:
                min_finder = []
                for category in self.headers:
                    key = self.items[category+user[category]]
                    min_finder.append((func[0]*key + func[1]) % func[2])
                each.append(min(min_finder))
            sig_mat.append(each)
        sig_mat = pd.DataFrame(sig_mat)

        for k in range(self.band_size):
            start_index = k * self.hash_size
            end_index = start_index + self.hash_size
            subset_df = sig_mat.iloc[:, start_index:end_index]
            self.signature_matrix.iloc[:, k] = subset_df.to_records(index=False)

    def neighboring(self):
        for k in range(self.band_size):
            hashed_items = {}
            for i in range(self.signature_matrix.shape[0]):
                key = self.signature_matrix.iloc[i, k]
                if key in hashed_items:
                    hashed_items[key].append(i)
                else:
                    hashed_items[key] = [i]
            self.neighbors.append(hashed_items)

    def find_neighbors(self, input_array):
        specific_user = []
        for func in self.hash_function:
            min_finder = []
            for category in self.headers:
                hash_key = category + input_array[category]
                if hash_key not in self.items:
                    self.items[hash_key] = self.item_num
                    self.item_num += 1

                key = self.items[hash_key]
                min_finder.append((func[0] * key + func[1]) % func[2])
            specific_user.append(min(min_finder))

        neighbors = []
        for k in range(self.band_size):
            start_index = k * self.hash_size
            end_index = start_index + self.hash_size
            each_band = tuple(specific_user[start_index:end_index])
            if each_band in self.neighbors[k]:
                neighbors = list(set(neighbors + self.neighbors[k][each_band]))
        var = list(self.output)[0]
        neighbor_output = self.output.iloc[neighbors, :][[var]]

        return neighbors, pd.value_counts(neighbor_output[var].values, normalize=True)

    def recommend_courses(self, classes, n, p):
        if p > n:
            print("Error.")
            quit()
        recommended_programs = {}
        rank = 1
        program_categories = []
        for k in range(classes.shape[0]):
            kth_value = classes.iloc[k]
            program_name = classes[classes == kth_value].index[0]
            if "Online" in program_name:
                online = "yes"
            else:
                online = "no"

            if len(recommended_programs) == n:
                break
            if len(recommended_programs) >= (n-p):
                if self.program_by_category[program_name] not in program_categories:
                    recommended_programs['Rank {}'.format(rank)]= {'name': program_name,
                                                                   'percentage': int(kth_value*100),
                                                                   'onlne': online,
                                                                   'dates': self.program_by_date[program_name],
                                                                   'wildcard': 'yes'}
                    program_categories.append(self.program_by_category[program_name])
                    rank += 1
            else:
                recommended_programs['Rank {}'.format(rank)] = {'name': program_name,
                                                                'percentage': int(kth_value*100),
                                                                'onlne': online,
                                                                'dates': self.program_by_date[program_name],
                                                                'wildcard': 'no'}
                program_categories.append(self.program_by_category[program_name])
                rank += 1

        return recommended_programs
