# py-lingo

Utilities for helping you deploy a subset of Scikit-Learn linear models in Go. See the 
`lingo` repository for more details.

This package is particularly focussed on saving linear models _for inference_ purposes.

The package has been tested and supports the following Linear Model variants:

* **LinearRegression**
* **LogisticRegression**
* **Ridge**
* **RidgeClassifier**
* **Lasso**
* **SGDRegressor**
* **SGDClassifier**

## Quickstart

You can install `py-lingo` with.

```bash
pip install py-lingo
```  

You'll then be able to import it in your code with:

```python
import pylingo
from sklearn.linear_model import LinearRegression

model = LinearRegression()

pylingo.dump(model, "model.h5")

loaded_model = pylingo.load("model.h5")
```
