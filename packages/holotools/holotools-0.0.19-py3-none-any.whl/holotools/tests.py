#!/usr/bin/env python3
'''Tests For Tools'''
from hbiop import *
from htrim import *


def window_test(file):
    '''test the sliding window'''
    d = fdict(file)
    td = {}
    for k,v in d.items():
        print(k)
        td[k]=sliding_window(v)
    print(td)
window_test('test_16.fna')
