'''
Desc: Tree class and methods

Authors:
    - Chance Nelson <chance-nelson@nau.edu>
'''


from taxid import Taxa


class Node:
    def __init__(self, data):
        self.data   = data
        self.children = []
    
    def addChild(self, child):
        self.children.append(child)

    def insert(self, data, parent):
        '''
        Desc: Insert a node

        Args:
            data: data to insert
            parent: parent of the node

        Returns:
            True, on successful insert.
            False, if parent cannot be found.
        '''
        stack = [self]
        while stack:
            cur_node = stack[0]

            # Check if this is the node we need
            if hash(cur_node.data) == parent:
                cur_node.children.append(Node(data)) 
                return True

            stack = stack[1:]
            for child in cur_node.children:
                stack.insert(0, child)

        return False
