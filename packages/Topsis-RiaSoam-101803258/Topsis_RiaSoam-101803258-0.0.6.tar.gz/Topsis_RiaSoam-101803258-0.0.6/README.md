topsis\_pckg
============

It is a Python package to find out the best value among the different
data using the mathematical calculations. \#\# Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install
this package.

``` {.bash}
pip install topsis_RiaSoam-101803258
```

About
-----

TOPSIS is an acronym that stands for 'Technique of Order Preference
Similarity to the Ideal Solution' and is a pretty straightforward MCDA
method. As the name implies, the method is based on finding an ideal and
an anti-ideal solution and comparing the distance of each one of the
alternatives to those

To get started quickly, just use the following:

``` {.bash}
from topis_pckg.topsis import topsis
topsis('inputfilename','Weights','Impacts','Outputfilename')
```

make ensure the weights and impacts should be in ""

eg: "1,1,1,1" and "+,-,+,-"

Pre-requisite
-------------

The data should be enclosed in the csv file. There must be more than 2
columns

Result
------

the output(outputfilename) is saved in the project folder with extra 2
columns with topsis score and rank.

Contributing
------------

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate:
https://github.com/ria-2511/topsis_pckg \#\# 
License
[MIT](https://choosealicense.com/licenses/mit/)
