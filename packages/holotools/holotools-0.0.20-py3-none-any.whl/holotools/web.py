import boto3
from boto3 import client
#upload blast file to s3
def s3_upload(file_name, bucket, s3_name):
    s3 = boto3.client('s3')
    s3.upload_file(file_name, bucket, s3_name)
#grab blast file from s3
def s3_download(file_name,bucket,s3_name):
    s3 = boto3.client('s3')
    s3.download_file(bucket, s3_name, file_name)
# process files from html post request and put them in s3
def process_files(request, files, file_store, s3, subfolder):
    lst = []
    for c, x in enumerate(request.FILES.getlist(files)):
        name = str(x)
        with open(file_store+name, 'wb+') as destination:
            for chunk in x.chunks():
                destination.write(chunk)
        lst.append(str(x)) #gets file names
        s3_upload(file_store+name, s3, subfolder+name)
    return lst

class Hasht(object):
    '''Hash Table For Consensus and MiniStock'''
    def __init__(self, dfp, dfc):
        # changing these to numpy matrix rather than pandas is faster
        self.dfp = dfp.to_numpy()
        self.dfc = dfc.to_numpy()
        self.dfpd = {}
        c=0
        for i in list(dfp):
            self.dfpd[i]=c
            c+=1
        self.dfcd={}
        c=0
        for i in list(dfc):
            self.dfcd[i]=c
            c+=1
        self.size = int((len(dfp)+len(dfc))*1.4)
        self.map = [None]*self.size

    def get_hash(self,key):
        hash = 0
        for char in str(key):
            hash+=ord(char)
        return hash % self.size

    def add (self, key, value):
        import math
        key_hash = self.get_hash(key)
        key_value = [key, value]
        if self.map[key_hash] is None:
            self.map[key_hash]= list([key_value])
            return True
        else:
            for pair in self.map[key_hash]:
                if pair[0]==key:
                    if math.isnan(pair[1][2])==True and math.isnan(value[2])==True:
                        pair[1] = value
                    # check which sequence is longer
                    if pair[1][2]<=value[2]:
                        pair[1] = value
                    return True
            self.map[key_hash].append(key_value)
            return True

    def get(self, key):
        key_hash = self.get_hash(key)
        if self.map[key_hash] is not None:
            for pair in self.map[key_hash]:
                if pair[0]==key:
                    return pair[1]
        return None

    def delete(self, key):
        key_hash = self.get_hash(key)
        if self.map[key_hash] is None:
            return False
        for i in range(0, len(self.map[key_hash])):
            if self.map[key_hash][i][0]==key:
                self.map[key_hash].pop(i)
                return True

    def print(self):
        print('Sequences')
        for item in self.map:
            if item is not None:
                print(str(item))

    def load(self):
        '''This itself removes redundancies via hashing'''
        import math
        for i in range(0, len(self.dfp)):
            d = self.dfp[i]
            if d[self.dfpd['ministock_name']] != None:
                if math.isnan(d[self.dfpd['hb']])==False:
                    self.add(d[self.dfpd['ministock_name']],
                             ['part',int(d[self.dfpd['hb']]),d[self.dfpd['trimmed_len']], i])
                else:
                    self.add(d[self.dfpd['ministock_name']],
                             ['part',d[self.dfpd['hb']],d[self.dfpd['trimmed_len']], i])
            elif d.hb != None and math.isnan(d.hb)==False and d.hb!=0:
                self.add(int(d[self.dfpd['hb']]),
                         ['part',d[self.dfpd['hb']],d[self.dfpd['trimmed_len']], i])
        # by adding consensus last we can ensure that the hash is updated for cons over part
        for i in range(0, len(self.dfc)):
            d = self.dfc[i]
            if d[self.dfcd['hb']] != None and math.isnan(d[self.dfcd['hb']])==False and d[self.dfcd['hb']]!=0:
                self.add(int(d[self.dfcd['hb']]),
                         ['cons',d[self.dfcd['ministock_name']],d[self.dfcd['sequence_len']], i])
            else:
                self.add(d[self.dfcd['hb']],
                         ['cons',d[self.dfcd['ministock_name']],d[self.dfcd['sequence_len']], i])
    def clean(self):
        '''This Matches Minis with their HB and removes partials if necessary'''
        import math
        conlist = []
        for i in self.map:
            # go through the map and ignore None
            if i != None:
                # there may be collision so this resolves it
                for j in i:
                    # ask if the seq is from the partial list
                    if j[1][0] == 'part':
                        # link hb for the partial
                        if self.get(j[1][1]) != None:
                            y = self.get(j[1][1])
                            self.add(j[1][1], [y[0], j[0],y[2],y[3]])
                    # if consensus just add to con list for next phase
                    else:
                        conlist.append(j[0])
        for i in conlist:
            # get the info
            j = self.get(i)
            # decide if we should start
            go = False
            try:
                if math.isnan(i)==False:
                    go =True
            except:
                go = True
            # if it looks good
            if go==True:
                # check if there is a ministock (or HB) partial and delete it
                if self.get(j[1]) != None and j[1]!=i and self.get(j[1])[0]=='part':
                    self.delete(j[1])


    def clean_df(self):
        self.load()
        self.clean()
        nd = []
        for i in self.map:
            if i !=None:
                for j in i:
                    if j[1][0] =='part':
                        md = 'partial'
                        d = self.dfp[j[1][3]]
                        try:
                            l = len(d[self.dfpd['trimmed_sequence']])
                        except:
                            l = 0
                        if d[self.dfpd['hb']] ==0:
                            hb = ''
                        else:
                            hb = d[self.dfpd['hb']]
                        nd.append([md,
                                   d[self.dfpd['date']],
                                   d[self.dfpd['quality']],
                                   d[self.dfpd['ministock_name']],
                                   hb,
                                   d[self.dfpd['hd']],
                                   d[self.dfpd['plate']],
                                   d[self.dfpd['working_stocks']],
                                   d[self.dfpd['species_1']],
                                   d[self.dfpd['strain_1']],
                                   d[self.dfpd['pct_1']],
                                   d[self.dfpd['nucnuc_1']],
                                   d[self.dfpd['species_2']],
                                   d[self.dfpd['strain_2']],
                                   d[self.dfpd['pct_2']],
                                   d[self.dfpd['nucnuc_2']],
                                   d[self.dfpd['media']],
                                   d[self.dfpd['treatment']],
                                   d[self.dfpd['enrichment']],
                                   l,
                                   d[self.dfpd['trimmed_ns']],
                                   d[self.dfpd['trimmed_sequence']],
                                  ])
                    else:
                        md = 'consensus'
                        d = self.dfc[j[1][3]]
                        try:
                            l = len(d[self.dfcd['sequence']])
                        except:
                            l = 0
                        if d[self.dfcd['hb']] ==0:
                            hb = ''
                        else:
                            hb = d[self.dfcd['hb']]
                        nd.append([md,
                                   d[self.dfcd['date']],
                                   d[self.dfcd['quality']],
                                   d[self.dfcd['ministock_name']],
                                   hb,
                                   d[self.dfcd['hd']],
                                   d[self.dfcd['plate']],
                                   d[self.dfcd['working_stocks']],
                                   d[self.dfcd['species_1']],
                                   d[self.dfcd['strain_1']],
                                   d[self.dfcd['pct_1']],
                                   d[self.dfcd['nucnuc_1']],
                                   d[self.dfcd['species_2']],
                                   d[self.dfcd['strain_2']],
                                   d[self.dfcd['pct_2']],
                                   d[self.dfcd['nucnuc_2']],
                                   d[self.dfcd['media']],
                                   d[self.dfcd['treatment']],
                                   d[self.dfcd['enrichment']],
                                   l,
                                   d[self.dfcd['sequence_ns']],
                                   d[self.dfcd['sequence']],
                                  ])
        import pandas as pd
        return pd.DataFrame(nd,columns = ['type','date','quality','ministock_name','hb','plate','hd','working_stocks','species_1','strain_1','pct_1', 'nucnuc_1','species_2','strain_2','pct_2', 'nucnuc_2', 'media','treatment','enrichment','sequence_length','sequence_ns','sequence'])
