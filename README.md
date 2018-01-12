# cbs-research

Locality sensitive hashing (LSH) maps nearby data points to the same code by using hash functions that collide for similar points. By analyzing neighbors' behaviors, we can build a predictive model for furture user behaviors.

### Data Structure
LSH requires the following data sturucture :
#### Input
| | Feature 1  | Feature 2 |---|Feature m|
| :---: | :---: | :---: | :---: | :---: |
| User 1 | category<sub>1, 1</sub> | category<sub>1, 2</sub>  |---| category<sub>1, m</sub> |
| User 2 | category<sub>2, 1</sub>  | category<sub>2, 2</sub>  |---| category<sub>2, m</sub> |
| ---| --- | --- |---|---|
| User n| category<sub>n, 1</sub> | category<sub>n, 2</sub> |---| category<sub>n, m</sub> |

Assuming User 31's zipcode is 10029 and Feature 2 contains user zipcodes, category<sub>31, 2</sub> must be 10029.<br>
category<sub>p, q</sub> have any values including NaN.

#### Output
| | Output  |
| :---: | :---: | 
| User 1 | output<sub>1</sub> | 
| User 2 | output<sub>2</sub>  | 
| ---| --- | 
| User n| output<sub>n</sub> | 

### Cross Validation Setup
By default, Accuracy class object splits data into 5 folds.

```python
import Accuracy
import LSH

data = Accuracy.CrossValidate(input, output, n_folds=5)
data.split()
```

### Parameter Tuning
LSH with minhash takes the number of hash functions within each band and the number of bands as parameters. In order to tune the parameters, we run the evaluation method for a range of integer values.
```python
tuned_param = list()
for i in range(2, 6):
    for j in range(2, 6):
        print(i, j)
        accuracy = data.evaluate_minhash(i, j)
        mean_score = accuracy['Mean'][0]
        if len(tuned_param) == 0:
            tuned_param = [i, j, mean_score]
        elif tuned_param[2] > mean_score:
            tuned_param = [i, j, mean_score]
print("best param: ", tuned_param[0], tuned_param[1])
```
We define success if user picks an item among recommended items and calculate accuracy.

### Prediction
After optimizing the parameters, we can fit a model and make a prediction for a specific user.
```python
lsh = LSH.MinHash(input, output, tuned_param[0], tuned_param[1])
lsh.train()
lsh.predict(test_input, num_of_items, num_of_categories)
print(trained_model.result['item'][0])
```
num_of_items is the number of predictions. num_of_categories For my research purposes, I added num_of_categories, so that I could increase coverages by making the predictions consist of items of different categories. If you do not care about item categories, just set it to 0.
