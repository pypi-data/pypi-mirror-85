#!/usr/bin/env python3
'''Binders and Tools for Clustering of Bacterial Sequences'''
def qiimeformat(fastafile):
    import re
    import holotools.biop as biop
    out = open('qiimenames_'+fastafile, 'w')
    d = biop.fdict(fastafile)
    for k,v in d.items():
        out.write('>%s\n%s\n'%(re.sub('[^a-zA-Z0-9\n\.]','.',str(k))+'_Holobiome',str(v).upper()))
    out.close()

def qiime2vsearch(clean_seqs = 'truncated.fna', pct = 0.987):
    import os
    import shutil
    try:
        os.mkdir('tmp')
    except:
        print('tmp directory already exists, will overwrite')
        shutil.rmtree('tmp')
        os.mkdir('tmp')
    # read in samps into qiimes frustrating archive format
    os.system("qiime tools import --input-path %s --output-path seqs.qza --type 'SampleData[Sequences]'"%(clean_seqs))
    print('read')
    # run vsearch
    os.system("qiime vsearch dereplicate-sequences --i-sequences seqs.qza --o-dereplicated-table table.qza --o-dereplicated-sequences rep-seqs.qza")
    print('derep')

    # get the actual info you want out of qiimes frustrating archive format output
    os.system("qiime vsearch cluster-features-de-novo --i-table table.qza --i-sequences rep-seqs.qza --p-perc-identity %f --o-clustered-table table-dn-%s.qza --o-clustered-sequences rep-seqs-dn-%s.qza"%(pct,str(pct),str(pct)))
    print('cluster')

    # unzip table-dn-0.987.qza to get at the biom file
    os.system('unzip table-dn-%s.qza -d tmp'%(str(pct)))
    print('unzip')

    # convert biom to tsv
    cwd = os.getcwd()
    oi = os.listdir(cwd+'/tmp')
    table_dir = cwd+'/tmp/'+oi[0]+'/data/feature-table.biom'
    os.system('biom convert -i %s -o %s.%s.table.from_biom.tsv --to-tsv'%(table_dir, clean_seqs,str(pct)))
    os.system('rm -r tmp')
