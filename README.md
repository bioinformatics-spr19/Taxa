## Synopsis

GenBank/RefSeQ Taxonomic Sequence Partitioning project allows for NCBI taxonomy data retrieve and parsing taxa into a tree.

## Code Example
python main.py
- Used to retrieve NCBI data.
- Parses the csv and uses Networkx to plot images

## Motivation
Taxonomy is the practice of identifying different organisms, classifying them into categories, and naming them. Taxonomists over the years have produced a hierarchy of groups of organisms.
Organisms are assigned to ranks based on the similarities and dissimilarities of their characteristics. We can also define groups of organisms alongside their ranks, these groupings are called taxa. Groupings are periodically disputed by taxonomists because the criteria defined for inclusion of a species in a taxon is just a well educated guess by taxonomists, until proven otherwise.
Modern molecular techniques are allowing us to better define a taxa groups. With taxa we can make taxonomic sequences to Graph complex networks of organisms. Where organisms are the nodes and the similarities between organisms are the links. Taxonomic sequences are better recognized as a phylogenetic trees.

## Installation
install project using the following github link https://github.com/bioinformatics-spr19/Taxa
install Networkx follow the give link for more information on how to install https://networkx.github.io/documentation/latest/install.html

## Running
```
python main.py <species taxid from nodes.dmp> ...
```
