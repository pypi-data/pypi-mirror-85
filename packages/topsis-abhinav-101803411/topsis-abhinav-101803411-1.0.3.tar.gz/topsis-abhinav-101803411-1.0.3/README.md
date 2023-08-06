# TOPSIS-Python

Submitted By: **Abhinav Narang 101803411**


<br>

## How to use this package:

This package can be run as in the following example:


### In Python notebook :
```
>>> import pandas as pd
>>> from topsis_py.topsis import topsis
>>> df = pd.read_csv('data.csv').values
>>> d = dataset[:,1:]
>>> w = [1,1,1,1]
>>> im = ["+" , "+" , "-" , "+" ]
>>> df = topsis(d,w,im)
```



