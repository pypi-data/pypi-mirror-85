#!/usr/bin/env python3
'''Binders for Barrnap'''

def barrnap(query):
    '''Takes in assembly returns barrnap results'''
    import os
    os.system('barrnap %s -outseq %s.barrnap.fa'%(query,query))
    return '%s.barrnap.fa'%query

def barparse16(query):
    '''Takes in a -ouseq of Barrnap'''
    from Bio import SeqIO
    d = {}
    count = 0
    with open(query, 'r') as h:
        for r in SeqIO.parse(h,'fasta'):
            if '16S' in r.description:
                d['%s_barrnap_%s.fa'%(query,str(count))]=str(r.seq)
                count+=1
    return d

def barblast(query, remove = True):
    '''Takes in assembly, runs barrnap, blasts all 16s found'''
    import os
    from holotools.blast import blast16, parseblast
    d = barparse16(barrnap(query))
    dfs = []
    for k,v in d.items():
        out = open(k, 'w')
        out.write('>%s\n%s\n'%(k,v))
        out.close()
        df = parseblast(blast16(k))
        dfs.append(df)
        if remove==True:
            os.system('rm %s'%k)
    return dfs
