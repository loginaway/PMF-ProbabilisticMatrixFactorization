# coding: utf-8 
# author: loginaway

import numpy as np
import re

class toolkit:
    def readConf(self, filename='../pmf.conf'):
        with open(filename, 'r') as f:
            text=f.read()
        trainset_pat=re.compile(r'trainset_name=(.*)\n')
        testset_pat=re.compile(r'testset_name=(.*)\n')
        stepsize_pat=re.compile(r'stepsize=(.*)\n')
        embedding_pat=re.compile(r'embedding_dimension=(.*)\n')
        epoch_pat=re.compile(r'epoch_num=(.*)\n')
        ku_pat=re.compile(r'k_u=(.*)\n')
        kv_pat=re.compile(r'k_v=(.*)\n')
        UVsize_pat=re.compile(r'UVsize=(.*)\n')
        ndcg_pat=re.compile(r'ndcg_top=(.*)\n')
        rmse_pat=re.compile(r'rmse=(.*)\n')
        
        conf={}
        conf['trainset']=trainset_pat.findall(text)[0].strip()
        conf['testset']=testset_pat.findall(text)[0].strip() if testset_pat.findall(text) else ''
        conf['stepsize']=eval(stepsize_pat.findall(text)[0].strip())
        conf['d']=eval(embedding_pat.findall(text)[0].strip())
        conf['epoch']=eval(epoch_pat.findall(text)[0].strip())
        conf['k_u']=eval(ku_pat.findall(text)[0].strip())
        conf['k_v']=eval(kv_pat.findall(text)[0].strip())
        conf['UVsize']=eval(UVsize_pat.findall(text)[0].strip())
        conf['NDCG']=eval('['+ndcg_pat.findall(text)[0]+']')
        conf['RMSE']=eval(rmse_pat.findall(text)[0])

        return conf

    def genfromtxt(self, filename):
        return np.genfromtxt(filename, dtype=np.float32)

    def generateRemark(self, size=(1,1), ratings=[[0,0,0]]):
        '''
        Generate R matrix at size=size, using data from ratings.
        Ratings: (n, 3) array with each row being a triple of User, Movie, Rating.
        '''
        R=np.zeros(size, dtype=np.float32)
        # print(ratings)
        for item in ratings:
            R[int(item[0]), int(item[1])]=item[2]

        return R

if __name__=='__main__':
    tk=toolkit()
    conf=tk.readConf()
    print(conf)

