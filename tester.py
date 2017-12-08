import pandas as pd
import Accuracy
import LSH
import pickle
import time
import pprint


def main():
    df = pd.read_csv("data/clean_data.csv", index_col=0)
    output = df[['Program Name']]
    df = df[['Company Size (group)', 'Industry Category (group)', 'Job Function (group)',
             'Position for Enrolled Only (group)', 'Years Work Experience (group)']]
    # data = Accuracy.CrossValidate(df, output, n_folds=5)
    # data.split()
    # tuned_param = list()
    # for i in range(2, 6):
    #     for j in range(2, 6):
    #         print(i, j)
    #         accuracy = data.evaluate_minhash(i, j)
    #         mean_score = accuracy['Mean'][0]
    #         if len(tuned_param) == 0:
    #             tuned_param = [i, j, mean_score]
    #         elif tuned_param[2] > mean_score:
    #             tuned_param = [i, j, mean_score]
    # print("best param: ", tuned_param[0], tuned_param[1])
    """
    Best Parameters are hash_size: 2 and band_size: 5
    """

    ## train using the whole dataset
    lsh = LSH.MinHash(df, output, 2, 5)
    lsh.train()
    pickle.dump(lsh, open("data/trained_model.p", "wb"))
    start = time.time()
    trained_model = pickle.load(open("data/trained_model.p", "rb"))
    end = time.time()
    print("loading: ", round(end - start, 3))

    test = {'Company Size (group)': '1-100',
            'Industry Category (group)': 'Finance',
            'Job Function (group)': 'General Management',
             'Position for Enrolled Only (group)': 'Manager',
            'Years Work Experience (group)': '1-20'}

    input = pd.DataFrame(test, index=[0])
    start = time.time()
    trained_model.predict(input, 5, 0)
    end = time.time()

    print("-------------------------------------------------")
    print("-------------------------------------------------")
    pprint.pprint(trained_model.result['item'][0])
    print("predict: ", round(end-start, 3))


if __name__ == "__main__":
    main()
