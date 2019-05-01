'''
Desc: Main file for the Taxa download and tree builder

Authors:
    - Chance Nelson <chance-nelson@nau.edu>
'''

import zipfile
import os
import sys

import networkx
import matplotlib.pyplot as plt

import download
from taxid import Taxa
from tree import Node


urls = ['ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdmp.zip']


def prepareData(url, path):
    '''
    Desc: Download the Taxa data files and unzip them into a working directory

    Args:
        url: url to download from
        path: path to download the taxa zip file to, then extract the needed 
              files into
    '''
    file_name = url.split('/')[-1]
    download.download(url, path + '/' + file_name)
    
    zip_f = zipfile.ZipFile(path + '/' + file_name)
    zip_f.extractall(path)
    zip_f.close()

def readTaxaData(path):
    '''
    Desc: Read the names list data from taxdump's 'names.dmp' file

    Args:
        path: path to the 'names.dmp' file

    Returns: Dictionary of a Taxa ID number to the actual name
    '''
    names = {}

    with open(path, 'r') as f:
        data = f.read().split('\n')

    for row in data:
        row = row.split('|')
        row = [i.strip() for i in row]

        if len(row) > 1:
            break

        names[int(row[0])] = row[1]

    return names


def readNodeData(path):
    '''
    Desc: Read the node list data from the taxdmp's 'nodes.dmp' file 

    Args:
        path: path to the 'nodes.dmp' file

    Returns: List of Taxa objects
    '''
    nodes = []

    with open(path, 'r') as f:
        data = f.read().split('\n')
        
    for row in data:
        row = row.split('|')
        row = [i.strip() for i in row]
        
        if len(row) <= 1:
            break

        tax_id   = row[0]
        tax_par  = row[1]
        tax_rank = row[2]

        nodes.append(Taxa(tax_id, tax_rank, tax_par))

    return nodes


def buildTree(nodes):
    '''
    Desc: Build a Taxonomy tree based on the retrieved Taxa data

    Args:
        nodes: list of Taxa objects

    Returns:
        Head node of a tree
    '''
    G = networkx.DiGraph()

    for node in nodes:
        n1 = int(node.taxid)
        n2 = int(node.parent)
        G.add_edge(n1, n2)

    return G


if __name__ == '__main__':
    # Create the working directory
    cwd = os.getcwd()
    path = cwd + '/.taxa_data'

    try:
        print("Checking for cached taxa data...", end='')
        sys.stdout.flush()
        os.mkdir(path)
        print(" Not found")
    
        print("Downloading and Preparing data...")
        sys.stdout.flush()
        prepareData(urls[0], path)

    except FileExistsError:
        print(" Found")
    

    print("Reading node list data...", end='')
    sys.stdout.flush()
    nodes = readNodeData(path + '/nodes.dmp')
    print(" Done")

    print("Building Taxonomy Tree...", end='')
    G = buildTree(nodes)
    print("Done")

    print("Generating plot...")
    networkx.draw_networkx(G)
    plt.show()
