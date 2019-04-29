'''
Desc: Main file for the Taxa download and tree builder

Authors:
    - Chance Nelson <chance-nelson@nau.edu>
'''

import zipfile
import os
import sys

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
    
    # Plan: create our head node from the first entry: Taxid with id 1
    head = Node(nodes[0])
    nodes.pop(0)

    print(len(nodes))

    print("sorting...")
    # Sort the node list, ordered by parent taxid
    nodes = sorted(nodes, key=lambda x: int(x.parent))
    print("sorted.")

    while nodes:
        # Attempt to insert
        if head.insert(nodes[0], int(nodes[0].parent)):
            print(nodes[0].parent, '->', nodes[0].taxid)
            nodes.pop(0)

        # Upon failure (parent node not in tree yet), move it to the back of
        # the queue, and continue
        else:
            nodes.append(nodes[0])
            nodes.pop(0)

    return head


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

    print("Building Taxonomy Tree...")
    head = buildTree(nodes)
    print("Done")
