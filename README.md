# Endpoint exposes service which generates unique cbtrees

## Requirements

```sh
# Check wether docker is installed by running
docker run hello-world
```

## Install

```sh
git clone https://github.com/adginr/cbtree-2023.git
# or via ssh
git clone git@github.com:adginr/cbtree-2023.git
```

## Run with docker `Recomended`

```sh
docker build -tag cbtree:latest
docker run -p 8080:8080 cbtree
```

[Try 127.0.0.1:8080](http://127.0.0.1:8080/docs)

## Alternative run

```sh

poetry install
poetry run uvicorn app.main:app --port 8080
```

```sh
# Not tested.
poetry export -f requirements.txt -o requirements.txt
pip install -r requirements.txt
uvicorn app.main:app --port 8080
```

[Try 127.0.0.1:8080](http://127.0.0.1:8080/docs)

### Run Pytest

```sh
pytest
```

## Description

CBTree - Constituency-based parse trees
[wiki](https://en.wikipedia.org/wiki/Parse_tree#Constituency-based_parse_trees)
NP - Noun Phrase

The core of over all processing is the `class ProcessTree` in 'app.service.process_tree'. Based on `nltk.tree.tree.Tree`.

**How does is work?**

1. On the very first step it looks for the tree positions that meet certain requirements: the node is `NP`, it's childs are also `NP` and separeted by either `,`(coma) or `CC` (and|or). The method `_get_nps` returns the list of node's position and its children positions. Hense it`s _possible to shuttle children with each other even if they are far away from each other_ (persist on the different branches).
2. Generating a set of possible positions
3. Applying the new positions to the tree and returning a string that represents the CBTree.
