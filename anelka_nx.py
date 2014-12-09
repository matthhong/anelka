from operator import itemgetter
import json
import networkx as nx

def import_data():
	with open('anelka.json') as infile:
		rawData = json.load(infile)
	return rawData

def simple_graph(rawData):
	G = nx.Graph()
	for item in rawData:
		try:
			y = int(item['date'][0])
		except:
			continue
		if item['fro'] in ["Unknown", "End of career", "Unemployed", "career break", "Own Under 19s", "eigene Jugend"]:
			continue
		elif item['to'] in ["Unknown", "End of career", "Unemployed","career break", "Own Under 19s", "eigene Jugend"]:
			continue
		elif int(item['date'][0]) >= 2013:
			G.add_edge(item['fro'], item['to'])
		else:
			pass
	return G

def max_centrality_key(G):
	C = nx.degree_centrality(G)
	return max(C.iteritems(), key=itemgetter(1))[0]