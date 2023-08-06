import pandas as pd
import numpy as np


class KnnMiss(object):
    def __init__(self, datas):
        self.datas = datas
        
    def get_miss(self):
        result = []
        miss_val = 0
        for data in self.datas:
            miss_data = self.datas[data].isnull()
            for i in miss_data:
                if i:
                    miss_val += 1
            print(f"{data}缺失{miss_val}个值！",end="")
            if miss_val:
                result.append(data)
            miss_val = 0
        if result is []:
            print("无缺失值！")

        return result

    def knn(self, miss_val):
        na_index=self.datas[self.datas[miss_val].isnull()].index.values
        normal_index = self.datas[~self.datas[miss_val].isnull()].index.values
        train_x = self.datas.iloc[normal_index]
        train_y = self.datas.iloc[normal_index,10]
        test_x = self.datas.iloc[na_index]
        test_y = self.datas.iloc[na_index,10]
        list(enumerate(train_x.iloc[:,2:3].values))
        distances = []
        for item in test_x.iloc[:,2:3].values: 
            dist = {}
            for index, item1 in enumerate(train_x.iloc[:,2:3].values):  
                distance = np.sqrt(np.sum(np.square(item - item1)))  
                dist[index] = distance 
            distances.append(dist)

        sorted_list = [sorted(item.items(), key = lambda x: x[1])[0:15] for item in distances]
        index_list =  [list(zip(*item_list))[0] for item_list in sorted_list]

        predict_var= {}
        for item in zip(na_index, index_list):
            predict_var[item[0]] = train_y.iloc[list(item[1])].mode()[0]

        datas[miss_val].fillna(predict_var,inplace=True)
    

    def deal_knn(self, miss_vals = None):
        miss_vals = self.get_miss()
        for miss_val in miss_vals:
            self.knn(miss_val)
        print(self.datas[1:11])    
        
        

# if __name__ == "__main__":

#     datas = pd.read_csv("filepath")
#     knn = KnnMiss(datas)
#     knn.deal_knn()
