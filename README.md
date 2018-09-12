# Boolean Query Model for IR

This is a Boolean Query Model for Information Retrieval in Python. Information retrieval is the activity of obtaining information system resources relevant to an information need from a collection of information resources. Searches can be based on full-text or other content-based indexing. We only implement text based indexing in this project. We use a Boolean Query Model to retrieve relevant information from our documents. The Boolean model of information retrieval is a classical information retrieval model and, at the same time, the first and most-adopted one. It is used by many IR systems to this day.

### Getting Started

To be able to run the search script, you'll need a few dependencies first:
```
pip install nltk
```

You also need to download and install [Python Algorithms Library](https://github.com/laurentluce/python-algorithms) from sources using:
```
cd python-algorithms/
python setup.py install
```

Once all that is done, change the `docs` and `stop_words` lists in `search.py` and get searching:

```
python search.py
```

### Results

```
~$ python search.py

INVERTED INDEX:

hello: [1, 2]
i: [1]
m: [1]
machin: [1, 4]
learn: [1, 4]
engin: [1, 2, 4]
bad: [2, 3]
world: [2, 3]
peopl: [2]
place: [3]
great: [4]
that: [4]

Enter boolean query: machine AND engineer
Processing time: 0.00031224 secs

Doc IDS:
[1, 4]

Enter boolean query: hello OR machine AND NOT engineer
Processing time: 0.00019799 secs

Doc IDS:
[1, 2]
```

### Built With

* Python
* NLTK