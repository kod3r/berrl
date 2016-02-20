'''
Module: pipegeojson.py 

A module to convert csv files representing geospatial features into appropriate geojson structures

Functions to be used:
1) read(location) - reads csv file to memory
2) get_cords_line(csvfile) - fault tolerant attempts to look at header in first row to get lat long structure within rows
3) get_segment_info(cordfile) - given a csv file and any unique identifier within a row will get data to be added in a format ready to go into akml
4) make_line(csvfile,**kwargs) - makes line object in geojson
5) 

Created by: Bennett Murphy
email: murphy214@marshall.edu
'''

import json
import itertools
import pandas as pd
import numpy as np
import os

#function that reads csv file to memory
def read(file):
	import csv
	data=[]
	f=csv.reader(open(file,'rb'),delimiter=',',quotechar="\"")
	for row in f:
		data.append(row)
	return data


#insert file name to get cordinates from
#fault tolerant attempts to look at header in first row to get lat long structure within rows
def get_cords_line(a):
	list=False
	#checking to see if the kwarg condition of inputting a list is given if so will evuate the var csvfile as if it is the list
	if list==False:
		segment=a
	else:
		segment=a
	cordblock=[]
	ind=0

	#getting header
	header=segment[0]

	#looking for lats, long and elevations within file
	#supports two points per line the most you would find for a path generally
	lats=[]
	longs=[]
	elevations=[]
	count=0
	for row in header:
		row=str(row).upper()
		if 'LAT' in str(row):
			lats.append(count)
		elif 'LONG' in str(row):
			longs.append(count)
		elif 'ELEV' in str(row):
			elevations.append(count)
		count+=1


	#if one lat and per row
	#FILETYPE OPTION: 1 LATITUDE, 1 LONGITUDE
	if len(lats)==1 and len(longs)==1 and len(elevations)==0:
		count=0
		cordrows=[]
		#getting the row numbers the latitude and longitude occur in
		rowlat1=lats[0]
		rowlong1=longs[0]

		#getting point to point rows for a flat (1 point row) csv file
		for row in segment[1:]: 
			if count==0:
				point=[row[rowlat1],row[rowlong1]]
				count=1
				newrow=point
			elif count==1:
				point=[row[rowlat1],row[rowlong1]]
				count=0
				newrow=newrow+point
				cordrows.append(newrow)

		#now going back through new list to parseinto connection points
		for row in cordrows:
			lat1=float(row[0])
			long1=float(row[1])
			lat2=float(row[2])
			long2=float(row[3])

			#making kml ready row to be appended into kml
			newrow=[long1,lat1]
			cordblock.append(newrow)
			newrow=[long2,lat2]
			cordblock.append(newrow)

	#FILETYPE OPTION: 1 LAT, 1 LONG, AND 1 ELEVATION
	elif len(lats)==1 and len(longs)==1 and len(elevations)==1:
		count=0
		cordrows=[]

		#getting the row numbers the latitude and longitude occur in
		rowlat1=lats[0]
		rowlong1=longs[0]
		rowele1=elevations[0]

		#getting point to point rows for a flat (1 point row) csv file
		for row in segment[1:]: 
			if count==0:
				point=[row[rowlat1],row[rowlong1],row[rowele1]] #lat,long,elevation
				count=1
				newrow=point
			elif count==1:
				point=[row[rowlat1],row[rowlong1],row[rowele1]] #lat,long,elevatioin
				count=0
				newrow=newrow+point
				cordrows.append(newrow)

		#now going back through new list to parseinto connection points
		for row in cordrows:
			lat1=float(row[0])
			long1=float(row[1])
			ele1=float(row[2])
			lat2=float(row[3])
			long2=float(row[4])
			ele2=float(row[5])

			newrow=[long1,lat1,ele1]
			cordblock.append(newrow)
			newrow=[long2,lat2,ele2]
			cordblock.append(newrow)

	#FILETYPE OPTION: 2 LAT, 2 LONG, AND 0 ELEVATION
	elif len(lats)==2 and len(longs)==2 and len(elevations)==0:
		count=0
		cordrows=[]

		#geting the row numbers for the lats, longs, and elevations
		rowlat1=lats[0]
		rowlong1=longs[0]
		rowlat2=lats[1]
		rowlong2=longs[1]

		for row in segment[1:]:
			lat1=row[rowlat1]
			long1=row[rowlong2]
			lat2=row[rowlat2]
			long2=row[rowlong2]

			newrow=[long1,lat1,0]
			cordblock.append(newrow)
			newrow=[long2,lat2,0]
			cordblock.append(newrow)

	#FILETYPE OPTION: 2 LAT, 2 LONG, AND 2 ELEVATIONS
	elif len(lats)==2 and len(longs)==2 and len(elevations)==2:
		count=0
		cordrows=[]

		#getting the row numbers for the lats,longs and elevations
		rowlat1=lats[0]
		rowlong1=longs[0]
		rowele1=elevations[0]
		rowlat2=lats[1]
		rowlong2=longs[1]
		rowele2=elevations[1]


		for row in segment[1:]:
			lat1=row[rowlat1]
			long1=row[rowlong1]
			ele1=row[rowele1]
			lat2=row[rowlat2]
			long2=row[rowlong2]
			ele2=row[rowele2]

			newrow=[long1,lat1,ele1]
			cordblock.append(newrow)
			newrow=[long2,lat2,ele2]
			cordblock.append(newrow)

	return cordblock


#given a csv file and any unique identifier within a row will get data to be added in a format ready to go into akml
#assumes the field name will be the corresponding title int he first (i.e. the header row)
def get_segment_info(data):
	csvfile=''
	uniqueindex=''
	list=False
	#checking to see if the kwarg condition of inputting a list is given if so will evuate the var csvfile as if it is the list
	if list==False:
		segment=data
	else:
		segment=data

	import itertools
	info=[]
	#getting segmentinfo if csv file is equal to '' and csvfile is equal to ''
	#this indictes that the segment info shouild be all likek values within the cordinate csv file
	if csvfile=='' and uniqueindex=='':
		header=segment[0]
		firstrow=segment[1]
		lastrow=segment[-1]

		for firstval,lastval,headerval in itertools.izip(firstrow,lastrow,header):
			if firstval==lastval:
				info.append([headerval,firstval])

	else:
		#setting up generators and getting header
		header=get_header(csvfile,list)
		next_row=gen_segment(csvfile,list)
		genuniqueindex=0
		
		#while statement that iterates through generator
		while not str(uniqueindex)==str(genuniqueindex):
			segmentrow=next(next_row)
			if str(uniqueindex) in segmentrow:
				for row in segmentrow:
					if str(row)==str(uniqueindex):
						genuniqueindex=str(row)
		
		#iterating through both header info and segment info to yield a list of both
		info=[]
		for headerval,segmentval in itertools.izip(header,segmentrow):
			info.append([headerval,segmentval])
		lastrow=segmentrow
	newrow=[]
	for row in lastrow:
		if 'NAN'in str(row).upper():
			row=str(row).upper()
		newrow.append(row)
	lastrow=newrow

	return [header,lastrow]


#makes a geojson line from a csv file or tabular list
def make_line(csvfile,**kwargs):
	#associating attributes with a specific region
	list=False
	strip=False
	jsonz=False
	outfilename=False
	remove_squares=False
	if kwargs is not None:
		for key,value in kwargs.iteritems():
			if key=='strip':
				if value==True:
					strip=True
			elif key=='list':
				if value==True:
					list=True
			elif key=='remove_squares':
				if value==True:
					remove_squares=True
			elif key=='outfilename':
				outfilename=str(value)

	if list==True:
		a=csvfile
		csvfile=outfilename
	else:
		a=read(csvfile)

	#changing dataframe to list if dataframe
	if isinstance(a,pd.DataFrame):
		a=df2list(a)
	count=0
	coords=[]
	newnewrow=[]
	for row in get_cords_line(a):
		if count==0:
			count=0
			newrow=[row[0],row[1]]
			coords.append(newrow)



	z=get_segment_info(a)
	#print json.dumps(dict(zip(['geometry: '],[dict(zip(['type: ','coordinates: '],['MultiLineString',[coords[:10]]]))])),indent=4)


	#getting properties
	a1=dict(zip(['properties'],['']))
	a2=dict(zip(z[0],z[1]))
	a3=dict(zip(['properties'],[a2]))


	#as of now witch craft that works
	c1=['geometry','properties']
	c2=dict(zip(['type','coordinates'],['LineString',coords[:]]))
	b=dict(zip(['geometry'],[dict(zip(['type','coordinates'],['LineString',coords[:]]))]))
	c=dict(zip(['type'],['Feature']))
	f=dict(zip(['type'],['FeatureCollection']))

	#as of now witchcraft that works
	e=dict(zip(c1,[c2,a2]))
	new=json.dumps(c,indent=7)[:-1]+json.dumps(e,indent=7)[2:]
	beg=['{ "type": "FeatureCollection",',
    '\t"features": [','  {  "type": "Feature",']
	gf=beg+[new[27:-1]]+['\t}','\t]']+[new[-1:]]


	return gf

#from a row and a given header returns a point with a lat, elevation
def getlatlong(row,header):
	import itertools
	ind=0
	lat=''
	long=''
	for a,b in itertools.izip(row,header):
		if 'LAT' in str(b).upper():
			lat=str(a)
			ind=1
		elif 'LONG' in str(b).upper():
			long=str(a)
			ind=1
		#this querries and parses the data for a 'location' string in the value position (i.e. lat and long with syntax '(lat, long)' or 'lat, long')
		'''
		elif 'LOCATION' in str(b).upper() and ind==0:
			val=str.split(str(a),',')
			if '(' in str(a) and ')' in str(a) and len(val)>2:
				lat=str(val[0])
				lat=lat[1:]
				long=str(val[1])
				long=long[1:-1]
			else:
				if len(val)==2:
					lat=str(val[0])
					long=str(val[1])
					if long[0]==' ':
						long=long[1:]
				else:
					lat=0
					long=0
					print lat,long
			'''
	return [float(lat),float(long)]


#makes a point geojson file
def make_points(csvfile,**kwargs):
	list=False
	strip=False
	outfilename=False
	remove_squares=False
	jsonz=True
	if kwargs is not None:
		for key,value in kwargs.iteritems():
			if key=='strip':
				if value==True:
					strip=True
			elif key=='list':
				if value==True:
					list=True
			elif key=='remove_squares':
				if value==True:
					remove_squares=True
			elif key=='outfilename':
				outfilename=str(value)
			elif key=='jsonz':
				if value==True:
					jsonz=True

	#checking for dataframe input
	if list==True:
		a=csvfile
	else:
		a=read(csvfile)

	#changing dataframe to list if dataframe
	if isinstance(a,pd.DataFrame):
		a=df2list(a)

	data=a
	total=[]
	header=data[0]
	for row in data[1:]:
		#iterating through each point in file
		latandlong=getlatlong(row,header)
		longandlat=[latandlong[1],latandlong[0]]
		if not str(longandlat[0]).upper()=='NAN' and not str(longandlat[1]).upper()=='NAN':

			oldrow=row
			newrow=[]
			for row in oldrow:
				if 'NAN'in str(row).upper():
					row=str(row).upper()
				newrow.append(row)
			oldrow=newrow


			#zipping the header and row
			info=dict(zip(header,oldrow))

			start=['{ "type": "FeatureCollection",','\t"features": [']

			#getting properties
			a1=dict(zip(['properties'],['']))
			a3=dict(zip(['properties'],[info]))


			#as of now witch craft that works
			c1=['geometry','properties']
			c2=dict(zip(['type','coordinates'],['Point',longandlat]))
			b=dict(zip(['geometry'],[dict(zip(['type','coordinates'],['LineString',longandlat]))]))
			c=dict(zip(['type'],['Feature']))
			f=dict(zip(['type'],['FeatureCollection']))

			#as of now witchcraft that works
			e=dict(zip(c1,[c2,info]))
			new=json.dumps(c,indent=7)[:-1]+json.dumps(e,indent=7)[2:]
			new=str.split(new,'\n')
			new=['\t{ "type": "Feature",']+new[2:-1]+['\t},']
			total+=new



	readytowrite=start+total[:-1]+['\t}','\t]','}']






	return readytowrite
	
#appends a list of lines to a geojson file
def parselist(list,location):
	f=open(location,'w')
	for row in list:
		f.writelines(row+'\n')
	f.close()
	print 'GeoJSON file written to location: %s' % location

# function for converting squares table to geojsonfile
def convertcsv2json(data,filename,**kwargs):
	shape=False
	strip=False
	outfilename=False
	remove_squares=False
	if kwargs is not None:
		for key,value in kwargs.iteritems():
			if key=='shape':
				if value==True:
					shape=True


	#creating a list
	newlist=[]

	#getting header
	header=data[0]

	#making the json rows
	if shape==False:
		for row in data[1:]:
			newlist.append(json.dumps(dict(zip(header,row)),indent=2))
	elif shape==True:
		newlist.append(json.dumps(dict(zip(header,data[1])),indent=2))


	#getting json filename
	if '/' in filename:
		filename=str.split(filename,'/')[1]

	newfilename=str.split(filename,'.')[0]+'.json'

	parselist(newlist,newfilename)

#given a set of table data returns the lat and longs associated with said tables
def getlatlongs(data):
	file=data

	#taking the following snippet from alignments.py
	#looking for lats, long and elevations within file
	#supports two points per line the most you would find for a path generally
	lats=[]
	longs=[]
	elevations=[]
	cordblock=[]
	count=0
	header=file[0]
	for row in header:
		row=str(row).upper()
		if 'LAT' in str(row):
			lats.append(count)
		elif 'LONG' in str(row):
			longs.append(count)
		elif 'ELEV' in str(row):
			elevations.append(count)
		count+=1


	#if one lat and per row
	#FILETYPE OPTION: 1 LATITUDE, 1 LONGITUDE
	if len(lats)==1 and len(longs)==1:
		count=0
		cordrows=[]
		#getting the row numbers the latitude and longitude occur in
		rowlat1=lats[0]
		rowlong1=longs[0]

		#getting point to point rows for a flat (1 point row) csv file
		for row in file[1:]: 
			point=[float(row[rowlat1]),float(row[rowlong1])]
			cordrows.append(point)
		return [['Lat','Long']]+cordrows
	elif len(lats)==4 and len(longs)==4:
		cordrows=[]
		cordrows2=[]
		for row in file[1:]:
			cordrows=[]
			for lat,long in itertools.izip(lats,longs):
				point=[float(row[lat]),float(row[long])]
				cordrows.append(point)
			cordrows2+=[cordrows]
		return [['Lat','Long']]+cordrows2

#given a set of data points from getlatlongs output returns north south east and west barrings to go into kml
def getextremas(data):
	points=getlatlongs(data)
	points2=points[1:]
	if len(points2)==1:
		points=pd.DataFrame(points2[0],columns=points[0])	
		south=points['Lat'].min()
		north=points['Lat'].max()
		west=points['Long'].min()
		east=points['Long'].max()
		return [east,west,south,north]
	return []

# writing a geojson implmentation thaat can have block csv files from pipegeohash directly
# see pipegeohash to get a general feel for the structure of each row in a csv file its pretty flexible mainly just requires 4 points (8 fields)
def make_blocks(csvfile,**kwargs):
	list=False
	strip=False
	outfilename=False
	remove_squares=False
	if kwargs is not None:
		for key,value in kwargs.iteritems():
			if key=='strip':
				if value==True:
					strip=True
			elif key=='list':
				if value==True:
					list=True
			elif key=='remove_squares':
				if value==True:
					remove_squares=True
			elif key=='outfilename':
				outfilename=value

	#checking for dataframe input
	if list==True:
		a=csvfile
		csvfile=outfilename
	else:
		#if list is equal to false reading the defualt assumed csvfile location
		a=read(csvfile)

	#changing dataframe to list if dataframe
	if isinstance(a,pd.DataFrame):
		a=df2list(a)


	start=['{ "type": "FeatureCollection",','\t"features": [']
	total=[]

	#getting header
	header=a[0]
	for row in a[1:]:
		#getting extremas
		extrema=getextremas([header,row])

		#now extrecting the point corners back out to be passed into a geojson file
		#I realize this is silly 
		point1=[extrema[0],extrema[-1]]
		point2=[extrema[1],extrema[-1]]
		point3=[extrema[1],extrema[-2]]
		point4=[extrema[0],extrema[-2]]

		#getting the cords list object from each corner point
		coords=[[point1,point2,point3,point4,point1]]

		#getting info or properties
		info=dict(zip(header,row))
		
		#using the same shit tier code that works I did before (this will be fixed)
		#as of now witch craft that works
		c1=['geometry','properties']
		c2=dict(zip(['type','coordinates'],['Polygon',coords]))
		b=dict(zip(['geometry'],[dict(zip(['type','coordinates'],['LineString',coords]))]))
		c=dict(zip(['type'],['Feature']))
		f=dict(zip(['type'],['FeatureCollection']))

		#as of now witchcraft that works
		e=dict(zip(c1,[c2,info]))
		new=json.dumps(c,indent=7)[:-1]+json.dumps(e,indent=7)[2:]
		new=str.split(new,'\n')
		new=['\t{ "type": "Feature",']+new[2:-1]+['\t},']
		total+=new

	readytowrite=start+total[:-1]+['\t}','\t]','}']
	return readytowrite

#makes a geojson line from a csv file or tabular list
def make_polygon(csvfile,**kwargs):
	#associating attributes with a specific region
	list=False
	strip=False
	jsonz=False
	outfilename=False
	remove_squares=False
	if kwargs is not None:
		for key,value in kwargs.iteritems():
			if key=='strip':
				if value==True:
					strip=True
			elif key=='list':
				if value==True:
					list=True
			elif key=='remove_squares':
				if value==True:
					remove_squares=True
			elif key=='outfilename':
				outfilename=str(value)


	if list==True:
		a=csvfile
		csvfile=outfilename
	else:
		a=read(csvfile)

	#changing dataframe to list if dataframe
	if isinstance(a,pd.DataFrame):
		a=df2list(a)
	count=0
	coords=[]
	newnewrow=[]
	for row in get_cords_line(a):
		if count==0:
			count=0
			newrow=[row[0],row[1]]
			coords.append(newrow)

	z=get_segment_info(a)
	#print json.dumps(dict(zip(['geometry: '],[dict(zip(['type: ','coordinates: '],['MultiLineString',[coords[:10]]]))])),indent=4)


	#getting properties
	a1=dict(zip(['properties'],['']))
	a2=dict(zip(z[0],z[1]))
	a3=dict(zip(['properties'],[a2]))


	#as of now witch craft that works
	c1=['geometry','properties']
	c2=dict(zip(['type','coordinates'],['Polygon', [coords]]))
	c=dict(zip(['type'],['Feature']))
	f=dict(zip(['type'],['FeatureCollection']))

	#as of now witchcraft that works
	e=dict(zip(c1,[c2,a2]))
	new=json.dumps(c,indent=7)[:-1]+json.dumps(e,indent=7)[2:]
	beg=['{ "type": "FeatureCollection",',
    '\t"features": [','  {  "type": "Feature",']
	gf=beg+[new[27:-1]]+['\t}','\t]']+[new[-1:]]

	return gf

#takes a dataframe and turns it into a list
def df2list(df):
	df=[df.columns.values.tolist()]+df.values.tolist()
	return df

#returns a list with geojson in the current directory
def get_geojsons(**kwargs):
	jsons=[]
	for dirpath, subdirs, files in os.walk(os.getcwd(str(dirs))):
	    for x in files:
	        if x.endswith(".geojson"):
	        	jsons.append(x)
	return jsons

#cleans the current of geojson files (deletes them)
def clean_current():
	jsons=get_geojsons()
	for row in jsons:
		os.remove(row)

#returns a list with geojson in the current directory
def get_filetype(src,filetype):
	filetypes=[]
	for dirpath, subdirs, files in os.walk(os.getcwd()+'/'+src):
	    for x in files:
	        if x.endswith('.'+str(filetype)):
	        	filetypes.append(src+'/'+x)
	return filetypes

