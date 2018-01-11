# cbs-research

Locality sensitive hashing (LSH) maps nearby data points to the same code by using hash functions that collide for similar points

### Data Structure
LSH requires the following data sturucture :

| | Feature 1  | Feature 2 |---|Feature m|
| :---: | :---: | :---: | :---: | :---: |
| User 1 | category<sub>1, 1</sub> | category<sub>1, 2</sub>  |---| category<sub>1, m</sub> |
| User 2 | category<sub>2, 1</sub>  | category<sub>2, 2</sub>  |---| category<sub>2, m</sub> |
| ---| --- | --- |---|---|
| User n| category<sub>n, 1</sub> | category<sub>n, 2</sub> |---| category<sub>n, m</sub> |

Assuming User 31's zipcode is 10029 and Feature 2 contains user zipcodes, category<sub>31, 2</sub> must be 10029.<br>
category<sub>p, q</sub> have any values including NaN.

### Cross Validation Setup

```python
import Accuracy
import LSH

data = Accuracy.CrossValidate(input, output, n_folds=5)
data.split()
```
