import pandas as pd
import numpy as np
import math


class topsis_main:
    def __init__(self, weights, impacts, df):
        self.arr = []
        self.weights = weights
        self.impacts = impacts
        self.df = df
        self.new_df = pd.DataFrame()

    def topsis(self):
        for i in range(0, len(self.weights)):
            self.weights[i] = self.weights[i]/sum(self.weights)
            if self.impacts[i] == "+":
                self.weights[i] = self.weights[i]
            else:
                self.weights[i] = self.weights[i]*-1


        rows, cols = np.shape(self.df)
        #Creating the dummy df to work on
        dummy = self.df.drop(self.df.columns[[0]],axis=1)
        dummy = np.asarray(dummy).astype("float32")
        rows = dummy.shape[0]
        cols = dummy.shape[1]
        for i in range(0,rows):
            for j in range(0,cols):
                dummy[i][j] = dummy[i][j]*self.weights[j]

        for j in range(1,cols):
            rss = 0
            for i in range(0,rows):
                rss += (dummy[i][j])**2
            rss = math.sqrt(rss)
            self.arr.append(rss)
        best = np.amax(dummy, axis=0)
        worst = np.amin(dummy,axis=0)


        sp = []
        sm = []
        for i in range(0,rows):
            sump=0
            summ=0
            for j in range(0,cols):
                sump += (dummy[i][j]-best[j])**2
                summ += (dummy[i][j] - worst[j])**2
            sp.append(math.sqrt(sump))
            sm.append(math.sqrt(summ))

        sp = np.asarray(sp)
        sp = sp.reshape((-1,1))
        sm = np.asarray(sm)
        sm = sm.reshape((-1,1))

        spm = sum(sp,sm)
        performance = np.divide(sm,spm)
        performance = performance.reshape((-1,1))
        dummy = np.append(dummy,sp,axis=1)
        dummy = np.append(dummy,sm,axis=1)
        dummy = np.append(dummy,spm,axis=1)
        dummy = np.append(dummy,performance,axis=1)
        #Creating the new df and setting up columns
        col_list = list(self.df.columns)[1:] + ["sp","sm","spm","performance"]
        self.new_df = pd.DataFrame(data = dummy,index = list(self.df.iloc[:,0]),columns = col_list)
        self.new_df = self.new_df.sort_values(['performance'],ascending="True")
        self.new_df["rank"]=[i for i in range(1,len(self.df)+1)]

        return self.new_df