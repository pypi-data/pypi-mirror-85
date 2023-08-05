#!/usr/bin/env python3
'''Binders and Tools for Clustering of Bacterial Sequences'''
def blastprimer(query, db='/home/boom/amp/primers/unambiguous_primers_2020.02'):
    import os
    cwd = os.getcwd()
    os.system('blastn -db %s -query %s -task "blastn-short" -out %s -outfmt 6'%(db,query,query+'.tsv'))

def blast16(query,outfmt = 6, db='/home/boom/Documents/holoweb/static/fasta/dbs/2020.02.C'):
    '''Std Output is BLAST tsv outfmt 6 (No Headers)'''
    import os
    cwd = os.getcwd()
    if outfmt == 0:
        os.system('blastn -db %s -query %s -out %s'%(db,query,query+'.txt'))
    else:
        os.system('blastn -db %s -query %s -out %s -outfmt %i'%(db,query,query+'.tsv',outfmt))
    return '%s.tsv'%query
def parseblast(file):
    '''tsv is expected'''
    import pandas as pd
    df = pd.read_csv(file,sep = '\t',header = None)
    df.columns = ['qseqid','sseqid','pident','length','mismatch','gapopen','qstart','qend','sstart','send','evalue','bitscore']
    df.sort_values(by='pident', ascending = False).reset_index()
    return df

def ifreverse(fasta):
    '''Reverse Complement of The Sequence If Necessary'''
    from Bio import SeqIO
    import holotools.blast as bl
    # fasta must be in its own .fa file
    bl.blast16(fasta,outfmt=0)
    txt = open(fasta+'.txt','r').readlines()
    for line in txt:
        if 'Strand=' in line:
            if 'Plus/Minus' in line:
                with open(fasta,'r') as h:
                    for r in SeqIO.parse(h,'fasta'):
                        x = r.seq.reverse_complement()
                return str(x), 'Reverse'
            else:
                with open(fasta,'r') as h:
                    for r in SeqIO.parse(h,'fasta'):
                        x = str(r.seq)
                return str(x), 'Forward'

def addsptofasta(fasta):
    '''take a multifasta, break it appart, blast each against 16s, add the species/pctid to the name, output new multifasta'''
    import os
    import shutil
    import holotools.biop as biop
    import sys
    cwd = os.getcwd()
    spfasta = open('spblast_'+fasta,'w')
    try:
        os.mkdir('tmp')
    except:
        print('tmp directory already exists, will overwrite')
        shutil.rmtree('tmp')
        os.mkdir('tmp')
    d = biop.fdict(fasta)
    n = len(d)
    c = 0
    for k,v in d.items():
        sys.stdout.write('\r')
        c+=1
        j = (c + 1) / n
        sys.stdout.write("[%-20s] %d%%" % ('~'*int(20*j), 100*j))
        sys.stdout.flush()
        out = open(os.getcwd()+'/tmp/'+k,'w')
        out.write('>%s\n%s\n'%(str(k),str(v)))
        out.close()
        try:
            blast16(cwd+'/tmp/'+k)
            df = parseblast(os.getcwd()+'/tmp/'+k+'.tsv')
            sp = df.sseqid.iloc[0]
            pid = df.pident.iloc[0]
            spfasta.write('>%s\n%s\n'%(k+'_'+sp+'_'+str(pid),str(v)))
        except:
            print('There was an issue with %s'%k)
    spfasta.close()
    shutil.rmtree('tmp')

def makeblastdb(dbtype, fasta, dbname):
    import os

    os.system('makeblastdb -dbtype %s -in %s -out %s'%(dbtype, fasta, dbname))

def protdna(dna_fasta,prot_db):
    '''take a dna assembly fasta and translate for all windows and blast against a protein db'''
    from Bio import SeqIO, Seq
    import os
    import pandas as pd
    dfs = []
    with open(dna_fasta) as h:
        for r in SeqIO.parse(h,'fasta'):
            start=[0,1,2]
            for s in start:
                tmp = r.description.replace(' ','_')+'_'+str(s)+'_f'+'.fasta'
                # forward
                fasta = open(tmp,'w')
                fasta.write('>%s\n%s'%(str(r.description.replace(' ','_')+'_'+str(s)+'_f'),str(r.seq[s:].translate())))
                fasta.close()
                os.system('blastp -db %s -query %s -out %s.tsv -outfmt 6'%(prot_db,tmp,tmp[:-6]+'_'+str(s)+'_f'))
                try:
                    df = pd.read_csv(tmp[:-6]+'_'+str(s)+'_f'+'.tsv',sep='\t')
                    df.columns = ['qseqid','sseqid','pident','length','mismatch','gapopen','qstart','qend','sstart','send','evalue','bitscore']
                    dfs.append(df.reset_index(drop=True))
                except:
                    print('no cols to parse %s %i f'%(r.description,s))

                # reverse
                tmp = r.description.replace(' ','_')+'_'+str(s)+'_r'+'.fasta'
                fasta = open(tmp,'w')
                fasta.write('>%s\n%s'%(str(r.description.replace(' ','_')+'_'+str(s)+'_R'),str(r.seq[::-1][s:].translate())))
                fasta.close()
                os.system('blastp -db %s -query %s -out %s.tsv -outfmt 6'%(prot_db,tmp,tmp[:-6]+'_'+str(s)+'_r'))
                try:
                    df = pd.read_csv(tmp[:-6]+'_'+str(s)+'_r'+'.tsv',sep='\t')
                    df.columns = ['qseqid','sseqid','pident','length','mismatch','gapopen','qstart','qend','sstart','send','evalue','bitscore']
                    dfs.append(df.reset_index(drop=True))
                except:
                    print('no cols to parse %s %i r'%(r.description,s))

                # os.remove(tmp[:-6]+'.tsv')
                # os.remove(tmp)
    dfs = pd.concat(dfs,axis=0, ignore_index = True)
    return dfs
