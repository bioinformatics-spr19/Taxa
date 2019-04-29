#!/usr/bin/env python


'''
Desc: Functions and classes for downloading files from the NCBI Taxa FTP server

Authors:
    - Chance Nelson <chance-nelson@nau.edu>
'''


import urllib.request
from tqdm import tqdm


class Download(tqdm):
    def update_for(self, b=1, bsize=1, tsize=None):
        if tsize:
            self.total = tsize

        self.update(b * bsize - self.n)


def download(url, out):
    with Download(unit='Bytes', unit_scale=True, miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=out, reporthook=t.update_for)
