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
import tree


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

        if not len(row) > 1:
            break

        names[int(row[0])] = row[1]

    return names


def readGencodeData(path):
    '''
    Desc: Read the gencode ID to sequence list in the 'gencode.dmp' file

    Args:
        path: path to the 'gencode.dmp' file

    Returns: dictionary of the gencode ID number to sequence
    '''
    sequences = {}

    with open(path, 'r') as f:
        data = f.read().split('\n')

    for row in data:
        row = row.split('|')
        row = [i.strip() for i in row]

        if not len(row) > 1:
            break

        sequences[int(row[0])] = row[3]

    return sequences


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
        gencode  = row[7]

        nodes.append(Taxa(tax_id, tax_rank, tax_par, gencode))

    return nodes


def buildTree(nodes, names, sequences):
    '''
    Desc: Build a Taxonomy tree based on the retrieved Taxa data

    Args:
        nodes: list of Taxa objects
        names: dictionary of taxid to names
        sequences: taxonomic sequences from gencode

    Returns:
        Head node of a tree
    '''
    G = networkx.DiGraph()

    for node in nodes:
        try:
            n1 = names[int(node.taxid)]

        except:
            n1 = int(node.taxid)

        try:
            n2 = names[int(node.parent)]

        except:
            n2 = int(node.parent)

        G.add_edge(n2, n1)

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
    taxa_nodes = readNodeData(path + '/nodes.dmp')
    print(" Done")

    print('Reading name list data...', end='')
    sys.stdout.flush()
    names = readTaxaData(path + '/names.dmp')
    print(' Done')
    
    print('Reading gencode list data...', end='')
    sys.stdout.flush()
    sequences = readGencodeData(path + '/gencode.dmp')
    print(' Done')

    print('Building Taxonomy Tree...', end='')
    sys.stdout.flush()
    G = buildTree(taxa_nodes, names, sequences)
    print(' Done')

    print('Generating example plot...')
    nodes = []
    for taxa in sys.argv[1:]:
        for i in taxa_nodes:
            if int(i.taxid) == int(taxa):
                print('Found GenCode Sequence for node ' + str(names[int(taxa)]) + ': ' + sequences[int(i.gencode_id)])

        try:
            nodes.extend(list(networkx.shortest_path(G, source=names[1], target=names[int(taxa)])))

        except:
            print('Error: Taxa ID not found (' + taxa + ')')

    subgraph = G.subgraph(nodes=nodes)
    networkx.draw_networkx(subgraph, pos=networkx.drawing.nx_agraph.graphviz_layout(subgraph))
    plt.show()
