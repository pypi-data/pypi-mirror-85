# TOPSIS-Python

Submitted By: **Abhimat Gupta 101983058**

***
pypi: <https://pypi.org/project/topsis-abhimat-101983058>
<br>
git: <https://github.com/abhi0444/topsis-abhimat-101983058.git>
***

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


