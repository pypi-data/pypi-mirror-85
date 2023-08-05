#!/usr/bin/env python3
'''Make Easier OS decisions'''
def getparent(p = True):
    import os
    this_file = os.path.abspath(__file__)
    this_dir = os.path.dirname(this_file)
    parent = os.path.abspath(os.path.join(this_dir, os.pardir))
    grandparent = os.path.abspath(os.path.join(parent, os.pardir))
    if p ==True:
        return parent
    else:
        return grandparent
