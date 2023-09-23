# Modality transition-based network from multivariate time series for characterizing horizontal oil–water flow patterns
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import warnings

warnings.filterwarnings("ignore")


class MTBCN:
    def __init__(self, multi_ts, L, W, S, file_path="network"):

        '''
        multi_ts: nparray - multivariate time series
        L: int - total hours
        W: int - windows size (hour)
        S: int - slide length
        file_path - str : save to here
        '''
        
        self.multi_ts = multi_ts
        self.L = L
        self. W = W
        self.S = S
        self.file_path = file_path

    # create modality
    def create_info(self):
        total_window = (self.L-self.W) // 2 + 1
        tmp = ""
        # record where tmp go to
        res = {tmp:[]}
        # i-th window
        for wdth in range(total_window):
            modality = ""
            # calculating the correlation coefficient
            l = [ts[wdth*self.S:wdth*self.S+self.W] for ts in self.multi_ts]
            r = np.corrcoef(l)
            l=[]
            for i in range(len(r)):
                for j in range(len(r)):
                    if i < j:
                        l.append(r[i,j])
            idx = [(value, index) for index, value in enumerate(l)]
            idx = sorted(idx, key=lambda x: x[0])
            for value, index in idx:
                modality += str(index)
            
            if modality not in res:
                res[modality] = []
    
            if tmp != modality:
                res[tmp].append(modality)
                
            tmp = modality
                            
        return res


    # visualization
    def plot(self, node_size = 500):
        
        self.res = self.create_info()
        edge_count = {}
        G = nx.DiGraph()

        for start, ends in self.res.items():
            for end in ends:
                if (start, end) in edge_count:
                    edge_count[(start, end)] += 1
                else:
                    edge_count[(start, end)] = 1
        
        for (start, end), count in edge_count.items():
            G.add_edge(start, end, label=str(count))
        
        pos = nx.spring_layout(G)
        labels = nx.get_edge_attributes(G, 'label')
    
        plt.figure(figsize=(10, 10))
        
        nx.draw(G, pos, with_labels=True, node_size=node_size, node_color='skyblue',
                font_size=8, font_color='black', font_weight='bold', arrows=True)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    
        plt.title("Modality Transition-Based Complex Network(MTBCN)")
        plt.axis('off')
        plt.savefig(self.file_path+".png")
        plt.show()