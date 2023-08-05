#!/usr/bin/env python3
'''Opporations That Should Be Standard'''
#how often symbol occurs in string
def occurs(symbol, string):
    return [j for j, x in enumerate(string) if x == symbol]
#random id generator of 6 figures
def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
