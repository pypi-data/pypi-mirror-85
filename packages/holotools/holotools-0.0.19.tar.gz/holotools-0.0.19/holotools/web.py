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
        self.dfp = dfp
        self.dfc = dfc
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
            d = self.dfp.iloc[i]
            if d.ministock_name != None:
                if math.isnan(d.hb)==False:
                    self.add(d.ministock_name,
                             ['part',int(d.hb),d.trimmed_len, i])
                else:
                    self.add(d.ministock_name,
                             ['part',d.hb,d.trimmed_len, i])
            elif d.hb != None and math.isnan(d.hb)==False and d.hb!=0:
                self.add(int(d.hb),
                         ['part',d.hb,d.trimmed_len, i])
            else:
                print(d)
        # by adding consensus last we can ensure that the hash is updated for cons over part
        for i in range(0, len(self.dfc)):
            d = self.dfc.iloc[i]
            if d.hb != None and math.isnan(d.hb)==False and d.hb!=0:
                self.add(int(d.hb),
                         ['cons',d.ministock_name,d.sequence_len, i])
            else:
                self.add(d.ministock_name,
                         ['cons',d.ministock_name,d.sequence_len, i])
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
                        d = self.dfp.iloc[j[1][3]]
                        try:
                            l = len(d.trimmed_sequence)
                        except:
                            l = 0
                        if d.hb ==0:
                            hb = ''
                        else:
                            hb = d.hb
                        nd.append([md,
                                   d.date,
                                   d.quality,
                                   d.ministock_name,
                                   hb,
                                   d.hd,
                                   d.plate,
                                   d.working_stocks,
                                   d.species_1,
                                   d.strain_1,
                                   d.pct_1,
                                   d.nucnuc_1,
                                   d.species_2,
                                   d.strain_2,
                                   d.pct_2,
                                   d.nucnuc_2,
                                   d.media,
                                   d.treatment,
                                   d.enrichment,
                                   l,
                                   d.trimmed_ns,
                                   d.trimmed_sequence,
                                  ])
                    else:
                        md = 'consensus'
                        d = self.dfc.iloc[j[1][3]]
                        try:
                            l = len(d.sequence)
                        except:
                            l = 0
                        if d.hb ==0:
                            hb = ''
                        else:
                            hb = d.hb
                        nd.append([md,
                                   d.date,
                                   d.quality,
                                   d.ministock_name,
                                   hb,
                                   d.hd,
                                   d.plate,
                                   d.working_stocks,
                                   d.species_1,
                                   d.strain_1,
                                   d.pct_1,
                                   d.nucnuc_1,
                                   d.species_2,
                                   d.strain_2,
                                   d.pct_2,
                                   d.nucnuc_2,
                                   d.media,
                                   d.treatment,
                                   d.enrichment,
                                   l,
                                   d.sequence_ns,
                                   d.sequence,
                                  ])
        import pandas as pd
        return pd.DataFrame(nd,columns = ['type','date','quality','ministock_name','hb','plate','hd','working_stocks','species_1','strain_1','pct_1', 'nucnuc_1','species_2','strain_2','pct_2', 'nucnuc_2', 'media','treatment','enrichment','sequence_length','sequence_ns','sequence'])
