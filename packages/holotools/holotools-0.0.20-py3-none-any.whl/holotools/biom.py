'''Biom Files Are Common Ways of Sharing Biological Data'''
class biom(object):
    '''Biom Info'''

    # initiate the file
    def __init__(self, file):
        self.file = file

    # load the file into model
    def read_tsv(self):
        '''load data into model'''
        # dependancies
        import pandas as pd
        # assume biom table is not clean
        try:
            print(biom)
            df = pd.read_csv(biom,sep = '\t')
        except:
            out = open('clean.%s'%(self.file),'w')
            x = open(self.file, 'r').readlines()
            [out.write(x[i]) for i in range(1,len(x))]
            out.close()
            df = pd.read_csv('clean.%s'%(self.file), sep = '\t')
            df['Total'] = df.sum(axis=1)

        self.df = df.sort_values(by='Total', ascending=False).reset_index(drop=True)

    # get the otu_fasta from qiime qza file
    def read_centroid_fasta(self):
        '''If Qiime2 Vsearch used the centroid names with the sequence names appended'''
        import os
        from Bio import SeqIO
        os.system('unzip rep-seqs.qza -d tmp')
        cwd = os.getcwd()
        oi = os.listdir(cwd+'/tmp')
        fasta_dir = cwd+'/tmp/'+oi[0]+'/data/dna-sequences.fasta'
        d = {}
        with open(fasta_dir,'r') as h:
            for r in SeqIO.parse(h,'fasta'):
                d[r.description]=str(r.seq)
        self.centroid_seqs = d
        os.system('rm -r tmp')

    def top(self, number):
        '''Returns a jupyter notebook interactive widget to view the sequences in the top n clusters'''
        # descriptions
        import ipywidgets as widgets
        from ipywidgets import Button, Layout
        from IPython.display import display
        # buttons
        df = self.df.sort_values(by = 'Total' )
        for i in range(0, number):
            button = widgets.Button(description='%s'%df['#OTU ID'][i],layout= Layout(width='50%'))
            output = widgets.Output()
            display(button, output)
            def on_button_clicked(b):
                with output:
                    from IPython.display import clear_output
                    clear_output()
                    df = self.df
                    row = df[df["#OTU ID"] == b.description].reset_index(drop=True)
                    # row = row.drop(['index'],axis =1)
                    lst = list(row)
                    lst.remove('#OTU ID')
                    lst.remove('Total')
                    toshow=[]
                    for j in lst:
                        if row[j][0]>0:
                            toshow.append(j)
                            print(j)
            button.on_click(on_button_clicked)

    def centroid_stats(self, print_stats = False):
        if print_stats == True:
            print('Centroid Stats\n\nAverage # Seqs to Centroid: \t%f\nStandard Deviation: \t\t%f\nMax Number Seqs to Centroid: \t%i\n'%(self.df.Total.mean(),self.df.Total.std(), self.df.Total.max()))
        return [self.file,self.df.Total.mean(),self.df.Total.std(), self.df.Total.max(), len(self.df.Total)]

    def in_seq_stats(self):
        '''If Qiime2 Vsearch used stats for the sequences that were put into the clustering program'''
        from Bio import SeqIO
        import numpy as np
        import os
        os.system('unzip seqs.qza -d tmp')
        cwd = os.getcwd()
        oi = os.listdir(cwd+'/tmp')
        fasta_dir = cwd+'/tmp/'+oi[0]+'/data/seqs.fna'
        d = {}
        lens = []
        ns = []
        with open(fasta_dir,'r') as h:
            for r in SeqIO.parse(h,'fasta'):
                d[r.description]=str(r.seq)
                lens.append(len(r.seq))
                ns.append(r.seq.count('N'))
        print('In Seq Stats\n\nAverage Length: %f\nStandard Deviation Length: %f\nAverage of Ns: %f\nStandard Deviation Ns: %f'%(np.mean(lens), np.std(lens), np.mean(ns), np.std(ns)))
        self.in_seqs = d
        os.system('rm -r tmp')

    def quicklist(self, centroidfasta = 'dna-sequences.fasta'):
        '''If Qiime2 Vsearch used Make an easy list out of the counts in each centroid'''
        import holotools.biop as biop
        import pandas as pd
        df = self.df
        new = []
        h = open(centroidfasta,'r').readlines()
        d = [i[1:-1] for i in h if '>' in i]
        for i in df["#OTU ID"]:
            for j in d:
                if i in j:
                    new.append(j)

        self.quick = pd.DataFrame([new,df.Total]).transpose()
        self.quick.columns= ['centroid','seq_count']
        self.df['newid']=new

    def clist(self):
        '''If Qiime2 Vsearch used this is a list of each sequence and the centroid it is in and the count of said centroid\nNote: quicklist must be used first'''
        import pandas as pd
        ndf = []
        self.df.index=self.df['newid']
        for i in self.df.index:
            x = ((self.df.loc[i]==1))
            for j in range(0,len(x)):
                if (x[j])==True and list(self.df)[j]!= 'Total':
                    ndf.append([i,list(self.df)[j],self.df['Total'][i]])
        ndf = pd.DataFrame(ndf, columns = ['centroid','seqid','total'])
        ndf.to_csv('clist.tsv',sep='\t', index = False)

    def singles(self):
        '''This is a list of the centroids with only one sequence in them'''
        s = self.df.loc[self.df.Total==1].reset_index(drop=True)
        singles = []
        for i in s.columns:
            try:
                if int(s[i].sum()) == 1:
                    singles.append(i)
            except:
                x=0
        self.singlelst = singles
        return singles
