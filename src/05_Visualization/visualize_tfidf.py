from pyvis.network import Network, Options
from pyvis.options import Configure
#from sklearn.preprocessing import LabelEncoder
import networkx as nx
import pandas as pd
import numpy as np

from calculate_tfidf import get_reichsanzeiger_docs_relation_matrix


class VisAnz_Net():

    def __init__(self, data_dict: dict, data_keywords: list(), height='750px', width='100%', bgcolor='#222222', font_color='white', verbose=False):
        self.data_dict = data_dict
        self.keywords = data_keywords
        #self.le = self.get_labelEncoder()
        self.net = self.get_pyvis_net(
            height=height, width=width, bgcolor=bgcolor, font_color=font_color)
        self.docs = self.get_docs()
        self.set_node_edge_data(verbose=verbose)

    def __eq__(self, other):
        other.net == self.net

    ''' def get_labelEncoder(self):
        le = LabelEncoder()
        le.fit(self.keywords)
        return le'''

    def get_docs(self):
        docs = [doc for doc in self.data_dict['context']]
        return docs

    def get_pyvis_net(self, height='750px', width='100%', bgcolor='#222222', font_color='white'):
        net = Network(height=height, width=width,
                      bgcolor=bgcolor, font_color=font_color)
        net.barnes_hut(gravity=-80000, central_gravity=0.3, spring_length=250,
                       spring_strength=0.001, damping=0.09, overlap=0)
        #net.force_atlas_2based(gravity=-80000, central_gravity=0.3, spring_length=250, spring_strength=0.001, damping=0.09, overlap=0)
        return net

    def set_node_edge_data(self, verbose=False):

        similarities = get_reichsanzeiger_docs_relation_matrix(
            docs=self.docs, verbose=verbose)
        #group_weights = get_reichsanzeiger_docs_relation_matrix(docs=self.docs, comp_data=self.keywords, verbose=verbose)
        #group_weights = np.argwhere(np.array(edge_weights).max(axis=1))
        #print('Group Weights:', group_weights)

        for i, value in enumerate(self.data_dict['id']):
            self.net.add_node(n_id=self.data_dict['id'][i], label=self.data_dict['name'][i],
                              title=self.data_dict['url'][i], group=self.data_dict['keyword'][i], physics=True)

        edge_threshold = 0.8

        for i in range(len(self.data_dict['id'])):
            for j in range(i):
                if i != j:
                    edge_weight = (similarities[i, j] + 1) / 2
                    if (edge_weight < edge_threshold):
                        self.net.add_edge(source=self.data_dict['id'][i], to=self.data_dict['id'][j],
                                          value=edge_weight*10, hidden=True, physics=True)
                    else:
                        self.net.add_edge(source=self.data_dict['id'][i], to=self.data_dict['id'][j],
                                          value=edge_weight*10, hidden=False, physics=True)

        # neighbor_map = self.net.get_adj_list()

        if verbose:
            print('Similarity Angles:', similarities)
            print('Edge_Threshold:', edge_threshold)

    def show_net(self, PATH_NET='VisualAnzeights.html'):
        self.net.toggle_physics(True)
        # self.net.set_options()
        # self.net.clustering.cluster()
        # Configure(enabled=True)
        self.net.show_buttons(filter_=['physics'])
        #self.net.repulsion(node_distance=100, central_gravity=0.2, spring_length=200, spring_strength=0.05, damping=0.09)
        self.net.show(PATH_NET)


if __name__ == '__main__':

    example_dict = {'id': [k for k in range(1, 21)],
                    'name': [f'News_Page {k}' for k in range(1, 21)],
                    'context': ['the house has a tiny little mouse',
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
                    'url': ['https://', 'https://', 'https://', 'https://', 'https://', 'https://', 'https://', 'https://', 'https://', 'https://',
                            'https://', 'https://', 'https://', 'https://', 'https://', 'https://', 'https://', 'https://', 'https://', 'https://'],
                    'keyword': ['House', 'House', 'House', 'House', 'House', 'House', 'House', 'House', 'House', 'House',
                                'Mouse', 'Mouse', 'Mouse', 'Mouse', 'Mouse', 'Mouse', 'Mouse', 'Story', 'Story', 'Story']
                    }

    keywords = ['House', 'Mouse', 'Story']

    visAnz_net = VisAnz_Net(example_dict, keywords)
    visAnz_net.show_net(
        PATH_NET='src/05_Visualization/Models/VisualAnzeights.html')
