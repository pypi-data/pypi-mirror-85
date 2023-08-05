#!/usr/bin/env python3
'''Tools For Trimming Sequences'''
def sliding_window(sequence,window_size = 20,max_number_ns = 2,max_ns_inarow = 2,min_len = 600,max_len = None,side = 'left',):
    '''Sliding Window With Specifications'''
    sequence = str(sequence)
    start = 0
    good_left = []
    left_gaps = []
    while start <= len(sequence) - window_size:
        window = sequence[start:start+window_size]
        if window.count('N')/window_size < max_number_ns/window_size and max_ns_inarow*'N' not in window:
            good_left.append(start)
        start+=1
    for i in range(0,len(good_left)-1):
        if good_left[i+1]-good_left[i]>1:
            left_gaps.append([good_left[i+1]-good_left[i], good_left[i],good_left[i+1]])
    dist = []
    if len(left_gaps)>1:
        for i in range(0,len(left_gaps)-1):
            dist.append(left_gaps[i+1][2]-left_gaps[i][2])
        if max(dist)>600:
            take = dist.index(max(dist))
            left = left_gaps[take][2]
            while sequence[left]=='N':
                left+=1
            if sequence[left:].index('N')<20:
                left += sequence[left:].index('N')+1
            right = left_gaps[take+1][1]+sequence[left_gaps[take+1][1]:].index('N')
        else:
            left = 0
            right = len(sequence)
    else:
        left = 0
        right = len(sequence)
    if right-left>600:
        qual = 'good'
    else:
        qual = 'bad'
    return {'left':left,'right':right,'seq':sequence[left:right]}
