# -*- coding: utf-8 -*-
import json
import numpy as np
from china_province import China_Province

class ChinaMap:
	provinceArray = China_Province().provinceArray

	def __init__(self):
		f = open("chinamap.json", 'r')
		geojson = f.read()
		self.geoinfo = json.loads(geojson)

	def allProvinces(self):
		xs = []
		ys = []
		for i in range(len(self.provinceArray)):	# because there are two hebei provinces, it is special on provinceArray list
			if self.provinceArray[i] == "河北":
				x, y = self.hebei()
				xs.extend(x)	# x = [1,2,3]  x.extend([4,5])=[1,2,3,4,5]
				ys.extend(y)
			else:
				x, y = self.province(self.provinceArray[i])
				xs.append(x)	# x = [1,2,3]  x.append([4,5])=[1,2,3,[4,5]]
				ys.append(y)
		return xs,ys

	def province(self, name):
		x = []
		y = []
		if name in self.provinceArray:
			index = self.provinceArray.index(name)
			coordinates = self.geoinfo["features"][index]["geometry"]["coordinates"][0]
			for i in range(len(coordinates)):
				x.append(coordinates[i][0])
				y.append(coordinates[i][1])

		return x, y

	def hebei(self):
		xs = []
		ys = []
		index = self.provinceArray.index("河北")	
		for j in range(2):		# because there are two Hebei provinces 
			x = []
			y = []
			coordinates = self.geoinfo["features"][index]["geometry"]["coordinates"][j][0]
			for i in range(len(coordinates)):
				x.append(coordinates[i][0])
				y.append(coordinates[i][1])
			xs.append(x)
			ys.append(y)
		
		return xs, ys

