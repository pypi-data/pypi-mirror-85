# The Curvature Method
[![Code Quality](https://www.code-inspector.com/project/16124/status/svg)](https://frontend.code-inspector.com/public/project/16124/curve_method/dashboard)
[![Build Status](https://travis-ci.org/alexjfreund/curve_method.svg?branch=main)](https://travis-ci.org/alexjfreund/curve_method)
[![codecov](https://codecov.io/gh/alexjfreund/curve_method/branch/main/graph/badge.svg)](https://codecov.io/gh/alexjfreund/curve_method)
[![PyPI version](https://badge.fury.io/py/curve-method.svg)](https://badge.fury.io/py/curve-method)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A quantitative approach to select the optimal number of clusters in a dataset.

## Table of contents
* [Introduction](#introduction)
* [Installation](#installation)
* [Examples](#examples)
* [Dependencies](#dependencies)
* [References](#references)
* [License](#license)

## Introduction

Clustering is a major area in Unsupervised Machine Learning. In many
clustering algorithms, the number of desired clusters is given as a
parameter. Selecting a dataset's true cluster number _k_ can be 
challenging, as model accuracy increases with additional clusters, yet 
too high of a _k_ value leads to overfitting, and a less meaningful model. 
Because the value of _k_ has a dramatic impact on clustering results, 
it is important to select it carefully.

The most common method of selecting a true cluster number is known as
the "Elbow Method", which involves manually selecting a point along an
evaluation graph that appears to contain the sharpest corner. There are
several problems with this approach, as it is empirical and requires direct
intervention. Additionally, the axes of the evaluation graph tend to lie on 
significantly different scales, which makes it difficult to recognize the 
optimal _k_ value visually. In contrast, the Curvature Method is a recent 
approach that quantitatively finds the optimal _k_ value [[1]](#1). This 
approach can be used in a broad range of clustering applications, further 
decoupling the learning process from human intervention.

## Installation
This project can be installed using pip:
```
pip install curve-method
```

## Examples
First, obtain a dataset as a 2D NumPy array. In these examples, we use the 
`make_blobs()` generator from Scikit-Learn to simulate a real dataset.
```python
from sklearn.datasets import make_blobs

X, _ = make_blobs(n_samples=10000, n_features=4, centers=5)
```

### Evaluation
To view the curvature index for each _k_ value up to a specified maximum, 
use the `curve_scores()` function.
```python
from curve_method import curve_scores

curve_scores(X, k_max=10)
```

Or, to obtain the _k_ value with maximum curvature, use the `true_k()` 
function.
```python
from curve_method import true_k

true_k(X, k_max=10)
```

### Plotting
To view the evaluation graph from the Curvature Method, use the 
`scatter()` function. If desired, points can be connected on the graph by 
setting `line=True`.
```python
from curve_method import scatter

scatter(X, k_max=12, line=False)
```

As an alternative, use the polyfit() function to generate an evaluation 
graph with a polynomial approximation. The degree of the polynomial _n_ 
can be specified by setting `deg=n`.
```python
from curve_method import polyfit

polyfit(X, k_max=12, deg=3)
```

## Dependencies
* NumPy
* Matplotlib
* Scikit-learn

## References
<a name="1"></a>
[1] Zhang, Y., Mańdziuk, J., Quek, C.H. and Goh, B.W., 2017.
Curvature-based method for determining the number of clusters.
Information Sciences, 415, pp.414-428.

## License
This project is licensed under the terms of the MIT License.