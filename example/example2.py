import berrl as bl
import pandas as pd
import numpy as np
import itertools

# please, if possible, don't abuse this key its not difficult to get your own
apikey='your api key'

# all the colors currently available for input
colors=['default','light green', 'blue', 'red', 'yellow', 'light blue', 'orange', 'purple', 'green', 'brown', 'pink']

# reading csv file to pandas
data=pd.read_csv('sharks.csv')

# mapping table to precision 4 geohashs
data=bl.map_table(data,3,list=True) # this creates a csv file with a density block table
squares=pd.read_csv('squares3.csv')
squares=squares[:10] # getting the top 10 densest geohash squares

# getting each unique geohash
geohashs=np.unique(squares['GEOHASH']).tolist()

# constructing list of all top shark attack incidents
total=[data.columns.values.tolist()]
for row in geohashs:
	temp=data[data.GEOHASH==str(row)] # getting all the geohashs within the entire table
	temp=bl.df2list(temp) # taking dataframe to list
	total+=temp[1:] #ignoring the header on each temporary list


# taking list back to dataframe
total=bl.list2df(total)

# getting the unique activities that occured
uniques=np.unique(total['Activity']).tolist()

# we now have a list with each top geohash in a aggregated table
# we can now style each color icon based on each activity being performed during the attack
count=0
filenames=[]
for unique,color in itertools.izip(uniques,colors):
	count+=1
	filename=str(count)+'.geojson' # generating a dummy file name
	temp=total[total.Activity==unique] 
	if not len(temp)==0: # if dataframe is empty will not make_points
		temp['color']=str(color) # setting specific color to object
		a=bl.make_points(temp,list=True) # making geojson object 
		bl.parselist(a,filename) # writing object to file
		filenames.append(filename)


# writing the squares table and setting color to red
squares['color']='red'
a=bl.make_blocks(squares,list=True)
bl.parselist(a,'squares.geojson')

# adding squares to filenames
filenames.append('squares.geojson')

#loading final html
bl.loadparsehtml(filenames,apikey,colorkey='color')
