import json

namesDict = {
u'Ajax ' : 'AJA',
u'Anderlecht ' : 'AND',
u'Arsenal ' : 'ARS',
u'Atletico ' : 'ATM',
u'Austria Wien ' : 'WIE', 
u'Barcelona ' : 'BAR',
u'Basel ' : 'BAS',
u'Bayern ' : 'BAY',
u'Benfica ' : 'SLB',
u'CSKA Moskva ' : 'CSK',
u'Celtic ' : 'CEL',
u'Chelsea ' : 'CHE',
u'Dinamo Zagreb ' : 'ZAG',
u'Dortmund ' : 'BVB',
u'Fenerbahce ' : 'FEN',
u'Galatasaray ' : 'GAL',
u'Juventus ' : 'JUV',
u'Kobenhavn ' : 'KOB',
u'Legia ' : 'LEG',
u'Leverkusen ' : 'B04',
u'Ludogorets ' : 'LUD',
u'Lyon ' : 'LYO',
u'Man. City ' : 'MNC',
u'Man. United ' : 'MNU',
u'Maribor ' : 'NKM',
u'Marseille ' : 'MAR',
u'Milan ' : 'MIL',
u'Napoli ' : 'NAP',
u'Olympiacos ' : 'OLY',
u'PAOK ' : 'PAO',
u'PSV ' : 'PSV',
u'Paris ' : 'PSG',
u'Pacos Ferreira ' : 'PAC',
u'Plzen ' : 'PLZ',
u'Porto ' : 'POR',
u'Real Madrid ' : 'RMA',
u'Real Sociedad ' : 'RSO',
u'Schalke ' : 'S04',
u'Shakhtar Donetsk ' : 'SHA',
u'Shakhter ' : 'SHK',
u'Steaua ' : 'STE',
u'Zenit ' : 'ZEN'}

def parse():
	gamesDict = {}
	with open('./anelka_UCL_names/names.json') as infile:
		games = json.load(infile)
	for g in games:
		gamesDict[str(g['gid'])] = namesDict[g['home']] + namesDict[g['away']]
		gamesDict[namesDict[g['home']] + namesDict[g['away']]] = str(g['gid'])
	return gamesDict

gamesDict = parse()
