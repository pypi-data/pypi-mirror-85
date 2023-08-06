# Project Description

 

### TOPSIS-PYTHON


Submitted By- Sayantan Pradhan(101803693)

And of course Dillinger itself is open source with a [public repository][dill]
 on GitHub.

### How to use


```
>>> import pandas as pd
>>> from TOPSIS-Sayantan-101803693.Topsis import topsis
>>> dataset = pd.read_csv('data.csv').values
>>> d = dataset.drop[columns = dataset.columns[0]]
>>> w = [1,1,1,1]
>>> im = ["+" , "+" , "-" , "+" ]
>>> topsis(d,w,im)
```



### Output

The output will be a file generated in your working directory with topsis score and rank.