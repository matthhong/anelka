from pandas import DataFrame
from parse_names import gamesDict
from parse_passes import parse
from matplotlib.backends.backend_pdf import PdfPages
from collections import defaultdict as ddict
import matplotlib.pyplot as plt
import networkx as nx

def df_to_graph(df):
    G = nx.from_numpy_matrix(df.values, create_using=nx.DiGraph())
    G = nx.relabel_nodes(G, dict(enumerate(df.columns)))
    weights = nx.get_edge_attributes(G, 'weight')
    invW = dict([(k, 1/float(v)) for (k,v) in weights.items()])
    nx.set_edge_attributes(G, 'distance', invW)
    return G

def all_passing_stats(pDict, func, weight = 'weight'):
    stats = ddict(dict)
    for team1 in pDict.keys():
        for team2 in pDict[team1].keys():
            G = df_to_graph(pDict[team1][team2])
            stats[team1][team2] = func(G, weight = weight)
    return stats

def sort_stats(stats):
    stats_list = []
    for k1 in stats.keys():
        for k2 in stats[k1].keys():
            stats_list.append((k1, k2, stats[k1][k2]))
    return sorted(stats_list, key=lambda tup: tup[2])

# def degree_distribution_plots(passingDict):
# 	pp = PdfPages('./Figures/degree_distribution_plots.pdf')
# 	for gid in range(2011739, 2011871):
# 		game = gamesDict[str(gid)]
# 		home = game[:3]
# 		away = game[3:6]
# 		homePassing = passingDict[home][away + str(1)]
# 		awayPassing = passingDict[away][home + str(2)]
# 		homeG = df_to_graph(homePassing)
# 		awayG = df_to_graph(awayPassing)
# 		homeInD = (homeG.in_degree(weight = 'weight'), home, 'IN')
# 		awayInD = (awayG.in_degree(weight = 'weight'), away, 'IN')
# 		homeOutD = (homeG.out_degree(weight = 'weight'), home, 'OUT')
# 		awayOutD = (awayG.out_degree(weight = 'weight'), away, 'OUT')
# 		for d in [homeInD, awayInD, homeOutD, awayOutD]:
# 			degDist = d[0].values()
# 			degDist.sort(reverse=True)
# 			plt.plot(degDist)
# 			plt.title(game + ', ' + d[1] + ', ' + d[2])
# 			pp.savefig()
# 			plt.clf()
# 	pp.close()

def relevant_stats(G):
	cloC = nx.closeness_centrality(G, distance = 'distance')
	betC = nx.betweenness_centrality(G, weight = 'distance')
	katC = nx.katz_centrality(G)
	eigC = nx.eigenvector_centrality(G)

	return

def directed_weighted_triangles_and_degree_iter(G, nodes=None, weight=None, motif = 'middleman'):
    """Modified to include just middleman motifs."""
    if G.is_multigraph():
        raise NetworkXError("Not defined for multigraphs.")

    if weight is None or G.edges()==[]:
        max_weight=1.0
    else:
        max_weight=float(max(d.get(weight,1.0) 
                             for u,v,d in G.edges(data=True)))
    if nodes is None:
        nodes_nbrs = G.adj.items()
    else:
        nodes_nbrs= ( (n,G[n]) for n in G.nbunch_iter(nodes) )

    for i,out_nbrs in nodes_nbrs:
        i_out_nbrs = set(out_nbrs)
        i_in_nbrs = set(n for n, nbrs in nodes_nbrs if i in set(nbrs))
        weighted_triangles=0.0
        for j in i_in_nbrs:
            wji=G[j][i].get(weight,1.0)/max_weight
            j_out_nbrs=set(G[j])
            for k in i_out_nbrs&j_out_nbrs:
                wik=G[i][k].get(weight,1.0)/max_weight
                wjk=G[j][k].get(weight,1.0)/max_weight
                weighted_triangles+=(wji*wik*wjk)**(1.0/3.0)
        if weight:
            out_deg = sum(attrs[weight] for k, attrs in out_nbrs.items())
        else:
            out_deg = sum(1 for k in out_nbrs.items())
            
        yield (i,out_deg,weighted_triangles)

def average_clustering(G, nodes=None, weight=None, count_zeros=True):
	c=clustering(G,nodes,weight).values()
	if not count_zeros:
		c = [v for v in c if v > 0]
	return sum(c)/float(len(c))

def clustering(G, nodes=None, weight=None):
    td_iter=directed_weighted_triangles_and_degree_iter(G,nodes,weight)

    clusterc={}

    for v,d,t in td_iter:
        if t==0 or d < 2:
            clusterc[v]=0.0
        else:
            clusterc[v]=t/float(d*(d-1))

    if nodes in G: 
        return list(clusterc.values())[0] # return single value
    return clusterc