#!/usr/bin/env python3
'''Truncate Sequences to primer locations'''
def truncate2primer(file, primerlist= '/home/boom/amp/primers/unambiguous_primers_2020.02.fna', db = '/home/boom/amp/primers/unambiguous_primers_2020.02', startprimers = ['515F_mod','518R'], endprimers = ['907R','904R','902R','895F','928F'], min_pct = 90, plusleft = 0, plusright = 0, min_len_pct = 80, side = 'both', deltmp = True):
    from holotools import biop
    import os
    import shutil
    import pandas as pd
    import sys
    cwd = os.getcwd()
    # temp file set up for data dumps and manipulation
    try:
        os.mkdir('tmp')
    except:
        print('tmp directory already exists, will overwrite')
        shutil.rmtree('tmp')
        os.mkdir('tmp')
    # read in query file
    d = biop.fdict(file)
    p = biop.fdict(primerlist)
    fdf = pd.DataFrame()
    na = open('nopfound.tsv','w')
    na.write('query\tissue\tdetails\n')
    trunc = {}
    # make tmp files of each seq blast and parse
    #progress bar
    n = len(d)
    c = 0
    for k,v in d.items():
        sys.stdout.write('\r')
        # the exact output you're looking for:
        c+=1
        j = (c + 1) / n
        sys.stdout.write("[%-20s] %d%%" % ('~'*int(20*j), 100*j))
        sys.stdout.flush()
        out = open('%s/tmp/%s.fna'%(cwd,k),'w')
        out.write('>%s\n%s\n'%(k,v))
        out.close()
        os.system('blastn -db %s -query %s -task "blastn-short" -out %s -outfmt 6'%(db,cwd+'/tmp/'+k+'.fna',cwd+'/tmp/'+k+'.tsv'))
        mmax = -1
        mmin = -1
        try:
            df = pd.read_csv(cwd+'/tmp/'+k+'.tsv', sep = '\t',header = None)
            df.columns = ['qseqid','sseqid','pident','length','mismatch','gapopen','qstart','qend','sstart','send','evalue','bitscore']
            df = df.loc[df.pident>=min_pct]
            # end primers
            s = df[df.sseqid.isin(endprimers)]
            for i in endprimers:
                plen = len(p[i])
                ep = s.loc[s.sseqid==i]
                ep = ep.loc[ep.length>=plen*(min_len_pct/100)]
                if len(ep)<1:
                    na.write(k+'\tprimer not found\t%s\n'%i)
                else:
                    mmax = min(ep.qstart)
                fdf = pd.concat([fdf,ep])
            # start primers
            s = df[df.sseqid.isin(startprimers)]
            for i in startprimers:
                plen = len(p[i])
                ep = s.loc[s.sseqid==i]
                ep = ep.loc[ep.length>=plen*(min_len_pct/100)]
                if len(ep)<1:
                    na.write(k+'\tprimer not found\t%s\n'%i)
                else:
                    mmin = max(ep.qend)
                fdf = pd.concat([fdf,ep])
        except:
            na.write(k+'\tprimer not found\tall\n')

        if side == 'right':
            if mmax != -1:
                trunc[k]=v[:mmax]
        elif side == 'left':
            if mmin != -1:
                trunc[k]=v[mmin:]
        elif side == 'both':
            if mmax != -1 and mmin !=-1:
                trunc[k]=v[mmin:mmax]
    if deltmp == True:
        shutil.rmtree('tmp')


    na.close()
    new = open('truncated_'+file,'w')
    for k,v in trunc.items():
        new.write('>%s\n%s\n'%(str(k),str(v)))
    new.close()
    return fdf, trunc

# truncate2primer('test16.fna')
