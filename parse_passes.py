"""
Matt Hong
anelka
31/MAR/2014
Functions for parsing data collection results from MTurk
"""

import csv
import json
from collections import defaultdict as ddict
from pandas import DataFrame, Series
from parse_names import gamesDict

nDict = {
		'First': 1,
		'Second': 2,
		'Third': 3,
		'Fourth': 4,
		'Fifth': 5,
		'Sixth': 6,
		'Seventh': 7,
		'Eighth': 8,
		'Ninth': 9,
		'Tenth': 10,
		'Eleventh': 11}
sDict = {
		'Home (left)': 0,
		'Away (right)': 1}
gDict = gamesDict
batches = './Data/finalData.csv'
keyDict = {
		11: 'LC',
		12: 'LA',
		13: 'MC',
		14: 'MA',
		15: 'SC',
		16: 'SA',
		17: 'TP'}

def get_passing_dict():
	passingDict = ddict(dict)
	for i in range(2011739, 2011871):
		game = gDict[str(i)]
		home = game[:3]
		away = game[3:6]
		dfHome, dfAway = parse(game)
		passingDict[home][away] = dfHome
		passingDict[away]['@' + home] = dfAway
	return passingDict

def parse(game, distribution = True, ignore = False):
	"""Formats relevant data in a CSV file into two DataFrames, one for each team"""
	homeDict = {}
	awayDict = {}
	allDistros = [] #These four variables are for error checking
	allTPs = []
	homeLastLen = [0]
	awayLastLen = [0]
	with open(batches, 'rU') as infile:
		reader = csv.reader(infile)
		reader.next()
		for row in reader:
			if gDict[row[27]] == game:
				home = game[:3]
				away = game[3:6]
				if row[29] == 'Home (left)':
					team = home
					myDict = homeDict
					myLastLen = homeLastLen
				else:
					team = away
					myDict = awayDict
					myLastLen = awayLastLen
				pid = row[34]
				TP = row[30][:5]
				distro = [int(n) for n in row[31].split(',')]
				allTPs.append(TP)
				allDistros.append(distro[:11])
				if myLastLen[-1] != len(distro):
					if myLastLen[-1] == 0:
						myLastLen.append(len(distro))
						pass
					else:
						print 'Comma Error:', game, row[27], row[28], row[29]
						print 'Check for time errors after fix'
				else:
					myLastLen.append(len(distro))
				longP = [int(n) for n in row[32].split(',')]
				medP = [int(n) for n in row[33].split(',')]
				shortP = [int(n) for n in row[35].split(',')]
				for pData in [longP, medP, shortP]:
					if pData[0] > pData[1]:
						print 'Pass Order Error:', game, row[27], row[28], row[29]
				if not ignore:
					if sum(distro) != sum([longP[0], medP[0], shortP[0]]):
						print 'Distribution Error:', game, row[27], row[28], row[29], sum(distro)
				myDict[pid] = distro[:11] + longP + medP + shortP + [TP]
				if distribution:
					myDict[pid] = myDict[pid][:11]
	if (len(homeDict.keys()) != 11) or (len(awayDict.keys()) != 11):
		print 'Incomplete Data:', game, gDict[game]
	homeSubs = homeLastLen[-1] - 11
	awaySubs = awayLastLen[-1] - 11
	if len(allDistros) != len(list(uniq(allDistros))):
		print 'Row Duplicate Error:', game, gDict[game], len(allDistros) - len(list(uniq(allDistros)))
		if len(set(allTPs)) - 1 != homeSubs + awaySubs:
			print 'Time Error:', game, gDict[game]
	df1 = DataFrame(homeDict)
	df2 = DataFrame(awayDict)
	for df in [df1, df2]:
		df = df.transpose()
		players = [int(n) for n in df.index]
		players.sort()
		ixDict = {}
		for i in range(11): #Making a dict for df.rename()
			ixDict[i] = players[i]
		if not distribution:
			ixDict.update(keyDict)
		df.rename(columns = ixDict, inplace = True)
		yield df

def uniq(llst):
	"""Returns a generator for the set of a list of lists"""
	lst = []
	for item in llst:
	    if item in lst:
	        continue
	    yield item
	    lst.append(item)

if __name__ == '__main__':
	for i in range(2011739, 2011871):
		try:
			home, away = parse(gDict[str(i)])
			with open('JSON-passes/' + str(i) + '-1', 'w') as outfile1, \
				open('JSON-passes/' + str(i) + '-2', 'w') as outfile2:
				json.dump(home.transpose().to_dict(), outfile1)
				json.dump(away.transpose().to_dict(), outfile2)
		except IndexError:
			print 'Missing', i