#!/usr/bin/env python3
'''Tools For Trimming Sequences'''
def sliding_window(sequence,window_size = 20,max_number_ns = 2,max_ns_inarow = 2,min_len = 600,max_len = None,side = 'left',):
    '''Sliding Window With Specifications: Takes in Sequence as String'''
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
            qual = 'good'
        else:
            qual = 'bad'
        take = dist.index(max(dist))
        left = left_gaps[take][2]
        while sequence[left]=='N':
            left+=1
        try:
            if sequence[left:].index('N')<20:
                left += sequence[left:].index('N')+1
        except:
            placeholder = 'No index which is good'
        right = left_gaps[take+1][1]+sequence[left_gaps[take+1][1]:].index('N')
    else:
        left = 0
        while sequence[left]=='N':
            left+=1
        try:
            if sequence[left:].index('N')<20:
                left += sequence[left:].index('N')+1
        except:
                placeholder = 'No index which is good'
        right = len(sequence)-1
        while sequence[right]=='N':
            right-=1
        if right-left >600:
            qual = 'good'
        else:
            qual = 'bad'
    d =  {  'seq':sequence,
            'tseq':sequence[left:right],
            'length':right-left,
            'qual':qual,
            'left':left,
            'right':right,}
    return d



def window_many(file,to = True,side='both',window_size = 20,max_number_ns = 2,max_ns_inarow = 2,min_len = 600,max_len = None):
    '''dictionary output from a multifasta input'''
    import holotools.biop as hb
    d = hb.fdict(file)
    td = {}
    for k,v in d.items():
        print(k)
        td[k]=sliding_window(v,side=side,window_size=window_size,max_number_ns=max_number_ns,max_ns_inarow=max_ns_inarow,min_len=min_len,max_len=max_len)
        if side == 'left':
            td[k]['tseq']=td[k]['seq'][td[k]['left']:]
        if side == 'right':
            td[k]['tseq']=td[k]['seq'][:td[k]['right']]
        if to==True:
            td[k]=td[k]['tseq']
    return td
