#!/usr/bin/env python3
'''Just Make Biopython Work With Less Key Strokes'''
from Bio import SeqIO
def fdict(file):
    '''parse fasta file to dictionary'''
    d = {}
    with open(file,'r') as h:
        for r in SeqIO.parse(h,'fasta'):
            d[r.description]=str(r.seq)
    return d
def csvtofasta(outfile='fastafromcsv.fna', minsize = 300, maxsize=1000000, file='MasterTable.csv',seqnamecol='sequence_name',seqcol='starting_sequence', sep = ','):
    import pandas as pd
    df = pd.read_csv(file, sep=sep)
    df = df.loc[df[seqcol]!='NONE'].reset_index()
    out = open(outfile,'w')
    for k,v in zip(df[seqnamecol],df[seqcol]):
        out.write('>%s\n%s\n'%(k,v))
    out.close()
    print('Your Fasta %s Has Been Created'%outfile)
