from pyvis.network import Network
import pandas as pd
import numpy as np

from calculate_tfidf import get_reichsanzeiger_docs_relation_matrix

class VisAnz_Net():

    def __init__(self, data :dict, height='750px', width='100%', bgcolor='#222222', font_color='white', verbose=False):
        self.data_dict = data
        self.net = self.get_pyvis_net(height=height, width=width, bgcolor=bgcolor, font_color=font_color)
        self.docs = self.get_docs()
        self.relation_matrix = get_reichsanzeiger_docs_relation_matrix(docs=self.docs, verbose=verbose)
        self.edge_data = self.get_edge_data(edge_threshold=edge_threshold, verbose=verbose)


    def get_docs(self):
        docs = [value['context'] for key,value in self.data_dict.items()]
        return docs

    def get_pyvis_net(self, height='750px', width='100%', bgcolor='#222222', font_color='white'):
        net = Network(height=height, width=width, bgcolor=bgcolor, font_color=font_color)
        net.barnes_hut()
        return net

    def get_edge_data(self, verbose=False):
        sources = [key for key in self.data_dict.keys()]
        targets = [key for key in self.data_dict.keys()]
        weights = self.relation_matrix

        edge_data = []
        edge_threshold = 0.5/len(sources)

        for i in range(len(sources)):
            for j in range(len(targets)):
                if i != j and weights[i,j] > edge_threshold:
                    edge_data.append([sources[i], targets[j], weights[i,j]])
        
        # edge_data = np.meshgrid(sources, targets, weights)
        if verbose: 
            print('Weights:', weights)
            print('Edge_Data:', edge_data)
            print('Edge_Threshold:', edge_threshold)

        return edge_data

    def show_net(self, PATH_NET='VisualAnzeights.html'):

        for e in self.edge_data:
            src = e[0]
            dst = e[1]
            w = e[2]

            self.net.add_node(src, src, title=src)
            self.net.add_node(dst, dst, title=dst)
            self.net.add_edge(src, dst, value=w)

        neighbor_map = self.net.get_adj_list()

        # add neighbor data to node hover data
        '''for node in self.net.nodes:
            node['title'] += ': ' + self.data_dict[]#' Neighbors:<br>' + '<br>'.join(neighbor_map[node['id']])
            node['value'] = len(neighbor_map[node['id']])'''

        for key, value in self.data_dict.items():
            self.net.get_node(key)['title'] += ': ' + value['url']


        self.net.toggle_physics(True)
        self.net.show_buttons(filter_=['physics'])
        self.net.show(PATH_NET)


if __name__ == '__main__':
    
    example_dict = {'News_Page 1' : {'context':'the cat see the mouse', 'url':'https:'},    
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
                }

    visAnz_net = VisAnz_Net(example_dict)
    visAnz_net.show_net(PATH_NET='src/05_Visualization/Models/VisualAnzeights.html')