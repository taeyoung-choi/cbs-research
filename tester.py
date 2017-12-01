import pandas as pd
import Accuracy
import LSH
import pickle

def main():
    df = pd.read_csv("data/clean_data.csv", index_col=0)
    output = df[['Program Name']]
    df = df[['Company Size (group)', 'Industry Category (group)', 'Job Function (group)',
             'Position for Enrolled Only (group)', 'Years Work Experience (group)']]
    # data = Accuracy.CrossValidate(df, output, n_folds=5)
    # data.split()
    # for i in range(2, 6):
    #     for j in range(2, 6):
    #         print(i, j)
    #         data.evaluate_minhash(i, j)
    """
    Best Parameters are hash_size: 2 and band_size: 5
    """

    ## train using the whole dataset
    # lsh = LSH.MinHash(df, output, 2, 5)
    # lsh.train()
    # pickle.dump(lsh, open('trained_model.p', 'wb'))
    trained_model = pickle.load(open("data/trained_model.p", "rb"))

    print(list(df))
    for item in list(df):
        print(set(df[item].tolist()))

    test = {'Company Size (group)' : '1-100',
            'Industry Category (group)' : 'Finance',
            'Job Function (group)' : 'General Management',
             'Position for Enrolled Only (group)' : 'Manager',
            'Years Work Experience (group)': '1-20'}

    input = pd.DataFrame(test, index = [0])
    trained_model.predict(input, 5, 1)
    print("-------------------------------------------------")
    print("-------------------------------------------------")
    print(trained_model.result['item'][0])

if __name__ == "__main__":
    main()