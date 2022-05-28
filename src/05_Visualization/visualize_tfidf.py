from pyvis.network import Network, Options
from pyvis.options import Configure
from sklearn.preprocessing import LabelEncoder
import networkx as nx
import pandas as pd
import numpy as np

from calculate_tfidf import get_reichsanzeiger_docs_relation_matrix

class VisAnz_Net():

    def __init__(self, data_dict :dict, keywords :list(), height='750px', width='100%', bgcolor='#222222', font_color='white', verbose=False):
        self.data_dict = data_dict
        self.keywords = keywords
        self.le = self.get_labelEncoder()
        self.net = self.get_pyvis_net(height=height, width=width, bgcolor=bgcolor, font_color=font_color)
        self.docs = self.get_docs()
        self.edge_data = self.get_edge_data(verbose=verbose)
    
    def __eq__(self, other):
        other.net == self.net

    def get_labelEncoder(self):
        le = LabelEncoder()
        le.fit(self.keywords)
        return le
        
    def get_docs(self):
        docs = [doc for doc in self.data_dict['context']]
        return docs

    def get_pyvis_net(self, height='750px', width='100%', bgcolor='#222222', font_color='white'):
        net = Network(height=height, width=width, bgcolor=bgcolor, font_color=font_color)
        net.barnes_hut(gravity=-80000, central_gravity=0.3, spring_length=250, spring_strength=0.001, damping=0.09, overlap=0)
        #net.force_atlas_2based(gravity=-80000, central_gravity=0.3, spring_length=250, spring_strength=0.001, damping=0.09, overlap=0)
        return net

    def get_edge_data(self, verbose=False):
                
        edge_weights = get_reichsanzeiger_docs_relation_matrix(docs=self.docs, verbose=verbose)
        #group_weights = get_reichsanzeiger_docs_relation_matrix(docs=self.docs, comp_data=self.keywords, verbose=verbose)
        #group_weights = np.argwhere(np.array(edge_weights).max(axis=1))
        #print('Group Weights:', group_weights)

        nodes = pd.DataFrame(self.data_dict)
        sources = nodes['id']
        targets = nodes['id']
        groups = nodes['main keyword']
        names = nodes['name']

        edge_data = []
        edge_threshold = 0.5/len(sources)

        for i in range(len(sources)):
            for j in range(len(targets)):
                if i != j and edge_weights[i,j] > edge_threshold:
                    edge_data.append([sources[i], targets[j], edge_weights[i,j], groups[i], groups[j],
                                      names[i], names[j]])
        
        for e in edge_data:
            src = int(e[0])
            dst = int(e[1])
            w = e[2]
            group_src=e[3]
            group_dst=e[4]
            name=e[5]
            name=e[6]

            
            self.net.add_node(src, src, title=name, group=group_src, physics=True)
            self.net.add_node(dst, dst, title=name, group=group_dst, physics=True)
            
            self.net.add_edge(src, dst, value=w)

        neighbor_map = self.net.get_adj_list()

        # add neighbor data to node hover data
        #for node in self.net.nodes:
            #node['title'] += ': ' + self.data_dict['url'] #' Neighbors:<br>' + '<br>'.join(neighbor_map[node['id']])
            #node['value'] = len(neighbor_map[node['id']])
        
        for i, node_id in enumerate(self.data_dict['id']):
            self.net.get_node(int(node_id))['title'] += ': ' + self.data_dict['url'][i]
        
        '''edge_data = {'source': [i for i in self.data_dict['id']], 
                     'target': [j for j in self.data_dict['id']]}'''
        
        # edge_data = np.meshgrid(sources, targets, weights)
        if verbose: 
            print('Weights:', edge_weights)
            print('Edge_Data:', edge_data)
            print('Edge_Threshold:', edge_threshold)

        return edge_data

    def show_net(self, PATH_NET='VisualAnzeights.html'):
        self.net.toggle_physics(True)
        #self.net.set_options()
        #self.net.clustering.cluster()
        Configure(enabled=True)
        self.net.show_buttons(filter_=['physics'])
        #self.net.repulsion(node_distance=100, central_gravity=0.2, spring_length=200, spring_strength=0.05, damping=0.09)
        self.net.show(PATH_NET)


if __name__ == '__main__':
    
    '''example_dict = {'News_Page 1' : {'context':'the cat see the mouse', 'url':'https:'},    
                'News_Page 2' : {'context':'the house has a tiny little mouse', 'url':'https:'},
                'News_Page 3' : {'context':'the mouse ran away from the house', 'url':'https:'},
                'News_Page 4' : {'context':'the cat finally ate the mouse', 'url':'https:'},
                'News_Page 5' : {'context':'the end of the mouse story', 'url':'https:'},
                'News_Page 6' : {'context':'hello mouse, arre you out of the house?', 'url':'https:'},
                'News_Page 7' : {'context':'there is a little house mouse next to you', 'url':'https:'},
                'News_Page 8' : {'context':'be aware of the cat, she is hungy in this story', 'url':'https:'},
                'News_Page 9' : {'context':'cats are hunters and love mice', 'url':'https:'},
                'News_Page 10' : {'context':'A mouse is a poor animal always in fear of been eaten', 'url':'https:'},
                'News_Page 11' : {'context':'Do not catch mice buy a cat', 'url':'https:'},
                'News_Page 12' : {'context':'A mouse can be a Spartakist, however, not a very strong one', 'url':'https:'},
                'News_Page 13' : {'context':'History is telling the stories about cats and mice for decades', 'url':'https:'},
                'News_Page 14' : {'context':'Not a single mouse has style, cats have it with abundance', 'url':'https:'},
                'News_Page 15' : {'context':'The story about a dog and a cat starts with the hunt for a bigger dream', 'url':'https:'},
                'News_Page 16' : {'context':'In my last dream a cat was chasing a mouse in my house', 'url':'https:'},
                'News_Page 17' : {'context':'Although I love dogs, my children want a cat. I cannot convince them', 'url':'https:'},
                'News_Page 18' : {'context':'There is a bright future ahead in which cats will take over the world and feed mice to the people', 'url':'https:'},
                'News_Page 19' : {'context':'Be alarmed, a tiny cat is alreay enabled to be your house hunter', 'url':'https:'},
                'News_Page 20' : {'context':'Finally, the cat story finds an end with a still living mouse', 'url':'https:'},
                }'''
    
    example_dict = {'id':[k for k in range(1,21)],
                    'name':[f'News_Page {k}' for k in range(1,21)],
                    'context':['the house has a tiny little mouse', 
                               'the mouse ran away from the house', 
                               'the cat finally ate the mouse', 
                               'the end of the mouse story', 
                               'hello mouse, arre you out of the house?', 
                               'there is a little house mouse next to you',
                               'be aware of the cat, she is hungy in this story',
                               'cats are hunters and love mice', 
                               'A mouse is a poor animal always in fear of been eaten', 
                               'Do not catch mice buy a cat',
                               'A mouse can be a Spartakist, however, not a very strong one', 
                               'History is telling the stories about cats and mice for decades',
                               'Not a single mouse has style, cats have it with abundance', 
                               'The story about a dog and a cat starts with the hunt for a bigger dream', 
                               'In my last dream a cat was chasing a mouse in my house',
                               'Although I love dogs, my children want a cat. I cannot convince them',
                               'There is a bright future ahead in which cats will take over the world and feed mice to the people',
                               'Be alarmed, a tiny cat is alreay enabled to be your house hunter', 
                               'Finally, the cat story finds an end with a still living mouse',
                               'Without a mouse no house and no story to tell'],
                    'url': ['https://','https://','https://','https://','https://','https://','https://','https://','https://','https://',
                            'https://','https://','https://','https://','https://','https://','https://','https://','https://','https://'],
                    'main keyword': ['House', 'House', 'House', 'House', 'House', 'House', 'House', 'House', 'House', 'House',
                                     'Mouse', 'Mouse', 'Mouse', 'Mouse', 'Mouse', 'Mouse', 'Mouse', 'Story', 'Story', 'Story']
                    }

    keywords=['House', 'Mouse', 'Story']

    visAnz_net = VisAnz_Net(example_dict, keywords)
    visAnz_net.show_net(PATH_NET='src/05_Visualization/Models/VisualAnzeights.html')