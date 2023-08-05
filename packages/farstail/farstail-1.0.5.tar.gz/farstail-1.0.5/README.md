# FarsTail: A Persian Natural Language Inference Dataset
<br>
<br>
Natural Language Inference (NLI), also called Textual Entailment, is an important task in NLP with the goal of determining the inference relationship between a premise p and a hypothesis h. It is a three-class problem, where each pair (p, h) is assigned to one of these classes: "ENTAILMENT" if the hypothesis can be inferred from the premise, "CONTRADICTION" if the hypothesis contradicts the premise, and "NEUTRAL" if none of the above holds.
<br>There are large datasets such as SNLI, MNLI, and SciTail for NLI in English, but there are few datasets for poor-data languages like Persian.
<br>Persian (Farsi) language is a pluricentric language spoken by around 110 million people in countries like Iran, Afghanistan, and Tajikistan. Here, we present the first relatively large-scale Persian dataset for NLI task, called FarsTail. A total of 10,367 samples are generated from a collection of 3,539 multiple-choice questions. The train, validation, and test portions include 7,266, 1,537, and 1,564 instances, respectively.
<br>
<br>


## Getting started with package
We have provided an API in the form of a python package to read and use FarsTail easier for persian and non-persian language researchers. In the following, we will explain how to use this package.
<br>
<br>You'll need Python 3.6 or higher.
### Installation
```
pip install farstail
```
### using
* Loading the original FarsTail dataset.
```python
from farstail.datasets import farstail
train_data, val_data, test_data = farstail.load_original_data()
```


* Loading the indexed FarsTail dataset.
```python
from farstail.datasets import farstail
train_ind, val_ind, test_ind, dictionary = farstail.load_indexed_data()
```


