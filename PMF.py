# coding: utf-8

'''
    This is an implementation of PMF algorithm for recommender systems.
'''

import numpy as np
from dataAPI import dataAPI
from matplotlib import pyplot as pyplot

class PMF(object):

    def __init__(self, stepsize, D_dimension, batchNum, epochNum, R, k_u, k_v, UVsize):
        self.stepsize=stepsize
        self.dim=D_dimension
        self.batchNum=batchNum
        self.epochNum=epochNum
        
        self.k_u=k_u
        self.k_v=k_v
        # initialize U and V, for efficiency, U and V are transposed,
        # as their storage in memory is by row 
        self.U=0.1*np.random.randn(UVsize[0], D_dimension)
        self.V=0.1*np.random.randn(UVsize[1], D_dimension)
        self.UVsize=UVsize
        self.R=R
        self.I=np.sign(R)
    
    def objectiveFunc(self, U, V):
        Pred=np.dot(U, V.T)
        sec1=np.vdot(self.I, (self.R-Pred)**2)
        sec2=np.linalg.norm(U, 'fro')
        sec3=np.linalg.norm(V, 'fro')
        return (sec1 + self.k_u*sec2 + self.k_v*sec3)/2

    def gradU(self, R):
        '''
        R: different from self.R, R is a matrix generated by part of
            the dataset
        '''
        gradU=np.empty_like(self.U)
        Pred_dot_I=np.dot(self.U, self.V.T)*self.I
        for i in range(len(self.U)):
            sec1=np.dot(self.I[i]*R[i], self.V)
            sec2=np.dot(Pred_dot_I[i], self.V)
            sec3=self.k_u*self.U[i]
            
            gradU[i]=-sec1+sec2+sec3
        return gradU

    def gradV(self, R):
        '''
        R: different from self.R, R is a matrix generated by part of
            the dataset
        '''
        gradV=np.empty_like(self.V)
        Pred_dot_I=np.dot(self.U, self.V.T)*self.I
        for j in range(len(self.V)):
            sec1=np.dot(self.I.T[j]*R.T[j], self.U)
            sec2=np.dot(Pred_dot_I.T[j], self.U)
            sec3=self.k_v*self.V[j]

            gradV[j]=-sec1+sec2+sec3
        return gradV

    def update(self, R, beta=0.6):
        '''
        Update U and V
        R: the ratings matrix generated by either testing or training set
        beta: the parameter from Armijo condition.
        '''
        t=self.stepsize

        gradU=self.gradU(R)
        gradV=self.gradV(R)

        updatedVal=self.objectiveFunc(self.U-t*gradU, self.V-t*gradV)

        while updatedVal>self.objectiveFunc(self.U, self.V):
            t=t*beta
            updatedVal=self.objectiveFunc(self.U-t*gradU, self.V-t*gradV)

        self.U=self.U-t*gradU
        self.V=self.V-t*gradV

    def RMSE(self, ratings):
        '''
        Compute Root Mean Square Error between ratings and results
        from training.
        ratings: numpy arrays with size being (n, 3), where each row
                is a triple of User-Index+1, Movie-Index+1, TrueRating
        '''
        tmp=0
        for i, j, Rij in ratings:
            tmp+=(np.vdot(self.U[i-1], self.V[j-1])-Rij)**2
        return np.sqrt(tmp/len(ratings))

    def fit(self, trainingSet, testingSet, beta=0.6):
        epoch=0
        rmse=np.empty(self.epochNum)
        training_R=self.generateRemark(self.UVsize, trainingSet)

        while epoch<self.epochNum:
            rmse[epoch]=self.RMSE(testingSet)
            print('Epoch:', epoch,' | ', 'RMSE:', rmse[epoch])
            self.update(training_R, beta=0.6)

            epoch+=1
        
        return rmse
        
    def generateRemark(self, size=(1,1), ratings=[[0,0,0]], fromFile=False):
        '''
        Generate R matrix at size=size, using data from ratings.
        Ratings: (n, 3) array with each row being a triple of User, Movie, Rating.
        '''
        R=np.zeros(size, dtype=int)
        for item in ratings:
            R[item[0]-1, item[1]-1]=item[2]

        return R

    def saveData(self, rmse=None, saveUV=True, saveRMSE=True):
        if saveUV:
            np.save('U_SVD.npy', self.U)
            np.save('V_SVD.npy', self.V)
            print('U, V saved')
        if saveRMSE:
            np.save('RMSE_SVD.npy', rmse)
            print('rmse saved')

    def DCG(self, true_Ri, model_Ri, k=5):
        '''
        true_Ri: true rates from user information
        model_Ri: Rates from PMF
        k: DCG will be computed by the top k rates
        '''
        order=np.argsort(model_Ri)[::-1]
        y_true=np.take(true_Ri, order[:k])
        gain=2**y_true-1
        discounts=np.log2(np.arange(len(y_true))+2)
        return np.sum(gain/discounts)

    def NDCG(self, true_R, model_R, k=5):
        scores=np.zeros((len(true_R), 1))
        count=0
        for i in range(len(true_R)):
            IDCGi=self.DCG(true_R[i], true_R[i], k)
            DCGi=self.DCG(true_R[i], model_R[i], k)
            # print(DCGi, IDCGi)
            if IDCGi and DCGi:
                scores[i]=DCGi/IDCGi
                count+=1
        return np.sum(scores)/count

if __name__=='__main__':
    api=dataAPI()
    ratings, UVsize=api.fetchRatings(fromDB=False)
    R=api.generateRemark(UVsize, ratings, fromFile=True)
    trainingSet=api.readTrainingSet()
    testingSet=api.readTestingSet()

    pmf=PMF(0.01, 30, 1, 4, R, 0.02, 0.02, UVsize)
    rmse=pmf.fit(trainingSet, testingSet)
    pmf.saveData(rmse)