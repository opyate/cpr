# Develop

```shell
pyenv virtualenv 3.9.6 climate-policy-radar-tech-test-3.9.6
pyenv activate climate-policy-radar-tech-test-3.9.6
pip install -r requirements.txt 
```

Run tests with

```shell
pytest
```

# Usage

To start with a fresh index (e.g. in case the CSV or schema changes), simply delete the directory `index_dir`.

Run with

```shell
uvicorn main:app --reload
```

Then do a search, e.g. [http://127.0.0.1:8000/?keywords=circular&keywords=decarbonisation](http://127.0.0.1:8000/?keywords=circular&keywords=decarbonisation)

API docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

# Analysis

The database is small, so indeces can be localised to nodes. For this reason, a file-based index is created with [Whoosh](https://whoosh.readthedocs.io/en/latest/intro.html).

To scale, I would consider PostgresQL full text search, and then Solr or ElasticSearch.

Practical considerations:
- you might want to err on the side of showing more search results, rather than fewer. Policy makers need *all* the info they can get.

## Jaccard

```python
def jaccard_similarity(str1: str, str2: str): 
    a = set(str1.split()) 
    b = set(str2.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))
```

It suggests Jaccard, but I'd rather use bm25 or tf-idf, which considers things like certain keywords being more frequent across all documents, and adjusting weights accordingly. Also, Jaccard is mostly used to find similarity between equal-ish things, like 2 documents, or 2 customers, not a document and a list of keywords.

Full text search engines and libraries tend to also come with useful pre-processing capabilities. For example, Jaccard shouldn't just be applied to a corpus as-is, as one should first perform lemmatisation to reduce words to the same root.

## Algorithms

- bm25 (the default, and [probably ok](https://www.quora.com/Aarkstore-Global-Text-Analytics-Market-Which-one-is-more-robust-between-tf-idf-and-BM25); has two free variables that [might need tweaking](https://www.elastic.co/blog/practical-bm25-part-3-considerations-for-picking-b-and-k1-in-elasticsearch))
- tf (term frequency, good for general text similarity)
- tf-idf (tf - inverse document frequency, good for search query relevance)
- cosine (similar to Jaccard, but takes into account repeated words; see arguments against Jaccard further down)
- word2vec
- plenty more, but not enough time to analyse

## Postgresql full text search

Uses [Porter stemmer](http://snowball.tartarus.org/algorithms/porter/stemmer.html) according to [this article](https://www.compose.com/articles/indexing-for-full-text-search-in-postgresql/).

## Notes on the spec

It will be optimal to get a few example queries with known best results, against which the implementation can be evaluated.

It wasn't specified whether policy search will be offered in other languages.

The search API will accept "keywords", not "phrases", so lemmatisation is likely not required.

It wasn't specified whether pagination and limited results were required, so we return all results at once. (It's a small database anyway.)
