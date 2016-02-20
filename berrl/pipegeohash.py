'''
This module is meant to be used in conjunction with pipekml however I could see how it could have other uses.

Module: pipegeohash.py

Purpose: A simple tool for geohashing an entire table at once,and allowing you to update your both corresponding tables simultaneously

Functions to be used:
1) map_table(csvfile,presicion)-given a csv file name and a presicion from (1 to 8) return the coresponding geohash
2) df2list(df)-takes a dataframe to a list
3) list2df(list)-takes a list and turn it into DataFrame
4) update_squares(slicedtable,csvfileofsquares)-given a table you just sliced and a csv file of squares returns the corresponding squares with the table slicedtable

Created by: Bennett Murphy
email: murphy214@marshall.edu
'''

import geohash
import numpy as np
import pandas as pd

#function that reads csv file to memory
def read(file):
	data=[]
	import csv
	f=csv.reader(open(file,'rb'),delimiter=',',quotechar="\"")
	for row in f:
		data.append(row)
	return data

#function that writes csv file to memory
def writecsv(data,location):
	import csv
	with open(location,'wb') as f:
		a=csv.writer(f,delimiter=',')
		for row in data:
			if row>=0:
				a.writerow(row)
			else:
				a.writerows(row)
	print 'Wrote csv file to location: %s' % location

#performs the intial mapping of the squares table then associates the hash and the count back to the intial table
def map_table(csvfile,presicion,**kwargs):
	import itertools
	if kwargs is not None:
		list=False
		for key,value in kwargs.iteritems():
			if key=='list':
				if value==True:
					list=True
	if list==True:
		data=csvfile
	else:
		data=read(csvfile)
	if isinstance(data, pd.DataFrame):
		data=df2list(data)
	count=0
	ind1=0
	ind2=0

	#identifying lat long headers
	for row in data[0]:
		if 'LAT' in str(row).upper() and ind1==0:
			latrow=count
			ind1=1
		elif 'LONG' in str(row).upper() and ind2==0:
			longrow=count
			ind2=1
		count+=1

	#grabbing header
	header=data[0]+['GEOHASH']

	hashedlist=[header]
	#iterating through each value in alist
	for row in data[1:]:
		try:
			hash=geohash.encode(float(row[latrow]),float(row[longrow]),presicion)
			hashedlist.append(row+[hash])
		except Exception:
			pass
	make_squares(hashedlist,presicion)
	return list2df(hashedlist)

#generator function
def gen(list):
	for row in list:
		yield row

# n**2 generator
def yield_row(list,id):
	gener=gen(list[1:])
	newrow=next(gener)
	ind=0
	while not id==newrow[0] and ind==0:
		try:
			newrow=next(gener)
			if newrow[0]==id:
				return newrow
		except StopIteration:
			return []
	return []

# makes the square output table 
def make_squares(data,presicion):
	import numpy as np
	import pandas as pd
	hashs=[]
	count=0
	boxes=[['HASH','LAT1','LONG1','LAT2','LONG2','LAT3','LONG3','LAT4','LONG4']]
	for row in data[1:]:
		#processing out the 4 points
		hashreturn=geohash.decode_exactly(row[-1])

		#getting lat and long datu
		latdatum=hashreturn[0]
		longdatum=hashreturn[1]

		#getting delta
		latdelta=hashreturn[2]
		longdelta=hashreturn[3]

		point1=[latdatum-latdelta,longdatum+longdelta]
		point2=[latdatum-latdelta,longdatum-longdelta]
		point3=[latdatum+latdelta,longdatum+longdelta]
		point4=[latdatum+latdelta,longdatum-longdelta]


		pointrow=[row[-1]]+point1+point2+point3+point4
		boxes.append(pointrow)
		hashs.append(row[-1])


	newlist=[['GEOHASH','LAT1','LONG1','LAT2','LONG2','LAT3','LONG3','LAT4','LONG4']]
	boxes=pd.DataFrame(boxes[1:],columns=newlist[0])
	boxes['COUNT']=1
	boxes=boxes.groupby(newlist[0],sort=True).sum()
	boxes=boxes.sort_values(by=['COUNT'],ascending=False)
	boxes.to_csv('squares'+str(presicion)+'.csv')

	return data

#given a list of sliced table and the squares previously made from it return a new square table to make_blocks from 
def update_squares(slicedtable,csvfileofsquares):
	squares=pd.read_csv(csvfileofsquares)
	if not isinstance(slicedtable, pd.DataFrame):
		slicedtable=pd.DataFrame(slicedtable[1:],columns=slicedtable[0])
	
	#getting header
	header=slicedtable.columns.values.tolist()
	columnlabel=header[-1]

	#getting unique hashs
	uniquehashs=np.unique(slicedtable[columnlabel]).tolist()
	#reading old sqaure csv file into memory
	oldsquares=read(csvfileofsquares)

	#getting newsquares from unique list
	newsquares=[oldsquares[0]]
	for row in uniquehashs:
		oldrow=row
		for row in oldsquares:
			if row[0]==oldrow:
				newsquares.append(row)

	return newsquares

#takes a dataframe and turns it into a list
def df2list(df):
	df=[df.columns.values.tolist()]+df.values.tolist()
	return df
#takes a list and turns it into a datafrae
def list2df(df):
	df=pd.DataFrame(df[1:],columns=df[0])
	return df

#in order to avoid a huge join operation if you want to pivot by the count of the groupby square table count use this function
#square csv is the square table
#x is the value that you want values greater then
def greaterthentable(data,squarecsv,x):
	if not isinstance(data, pd.DataFrame):
		data=pd.DataFrame(data[1:],columns=data[0])

	square=read(squarecsv)
	header=data.columns.values.tolist()
	total=[header]
	for row in square[1:]:
		if int(row[-1])>int(x):
			temp=data[(data.GEOHASH==str(row[0]))]
			temp=temp.values.tolist()
			total+=temp
	return list2df(total)






