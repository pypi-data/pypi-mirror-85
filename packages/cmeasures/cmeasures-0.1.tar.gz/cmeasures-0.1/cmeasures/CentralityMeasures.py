import csv
import networkx as nx
import time

class CentralityMeasures:
    def getCentralityMeasures(EdgeList):
        Edges = open(EdgeList, 'r')
        next(Edges, None)
        f = open('Centrallity.txt', 'a')
        Graphtype = nx.DiGraph()
        G = nx.parse_edgelist(Edges, delimiter=';', create_using=Graphtype, nodetype=int)

        start_time = time.time()
        Deg = nx.degree_centrality(G)
        print('Degree:', time.time() - start_time)
        with open('Degree_Centrality.csv', 'w') as f:
            w = csv.writer(f)
            w.writerows(Deg.items())

        start_time = time.time()
        PR = nx.pagerank(G)
        print('PageRank:', time.time() - start_time)
        with open('Closeness_Centrality.csv', 'w') as f:
            w = csv.writer(f)
            w.writerows(PR.items())

        start_time = time.time()
        HUB, AUTH = nx.hits(G)
        print('HITS:', time.time() - start_time)
        with open('HITS_HUB_SCORES.csv', 'w') as f:
            w = csv.writer(f)
            w.writerows(HUB.items())
        with open('HITS_AUTHORITY_SCORES.csv', 'w') as f:
            w = csv.writer(f)
            w.writerows(AUTH.items())

        start_time = time.time()
        Btw = nx.betweenness_centrality(G)
        print('Betweenness:', time.time() - start_time)
        with open('Betweenness_Centrality.csv', 'w') as f:
            w = csv.writer(f)
            w.writerows(Btw.items())

        start_time = time.time()
        Clsn = nx.closeness_centrality(G)
        print('Closeness:', time.time() - start_time)
        with open('Closeness_Centrality.csv', 'w') as f:
            w = csv.writer(f)
            w.writerows(Clsn.items())