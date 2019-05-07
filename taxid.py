'''
Desc: Data structure to hold and preserve Taxa data

Authors:
    - Chance Nelson <chance-nelson@nau.edu>
'''


class Taxa:
    def __init__(self, taxid, rank, parent, gencode_id):
        self.taxid      = taxid
        self.rank       = rank
        self.parent     = parent
        self.gencode_id = gencode_id

    def __hash__(self):
        return int(self.taxid)

    def __eq__(self, other):
        if other.taxid == self.taxid:
            return True

        else:
            return False
