from PMF.PMF import PMF
from PMF.toolkit import toolkit
import numpy as np

api=toolkit()
conf=api.readConf('./pmf.conf')

trainset=api.genfromtxt(conf['trainset'])
testset=api.genfromtxt(conf['testset'])
ratings=np.concatenate((trainset, testset))

R=api.generateRemark(conf['UVsize'], ratings)


pmf=PMF(conf['stepsize'], conf['d'], conf['epoch'], R, conf['k_u'], conf['k_v'], conf['UVsize'])
rmse=pmf.fit(trainset, testset)
if conf['NDCG']:
    model_R=np.dot(pmf.U, pmf.V.T)
    ndcg_values=[]
    for ndcg_top_index in conf['NDCG']:
        ndcg_values.append(pmf.NDCG(pmf.R, model_R, ndcg_top_index))

if conf['RMSE']:
    conf['RMSE']=rmse[-1]
if conf['NDCG'] is not None:
    conf['NDCG']=ndcg_values
pmf.saveData(conf['RMSE'], conf['NDCG'])

