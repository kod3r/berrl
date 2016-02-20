### berrl - MapBox map output made simple with Python data structures
![](https://cloud.githubusercontent.com/assets/10904982/13199289/86ce2388-d7ef-11e5-856e-731d8212d2b4.png)

#### What is it?
This repository is a combination of 3 repositories I've previously made for geospatial data analysis. These modules I often found myself using in conjuction with one another and figured it would be useful to make an intuitive all in one repository to take full advantage and simplify the work I've already done. The general premise is keep things static enough to where pandas data structures can be integrated in a simple and intuitive manner by making some general assumptions about how the data will be inputted. The main asssumptions being: all geospatial fields will contain 'LAT','LONG', or 'ELEV' for their representive geo fields, and assuming that points and blocks (geohashed squares) can be input in multiples (i.e. each row is 1 element) and that polygons and linestrings are input one element at a time but still in tabular style. 

Instead of using functions made for JS and ported to Python I do the reverse making pandas dataframes able to be directly input and parsed correctly into geojson and styled generally how I desire it.By doing this one can put the geospatial analysis on the shoulders of pandas and numpy and put a lot of the hang ups when dealing with geospatial data to the side or at least make them static enough to negate a lot of the confusion. 

#### What about the HTML/JavaScript side of mapping?
Collecting all the geojson locations as you make them and inputting a color field kwarg allows you to style/pipe data into the correct HTML by simply "peaking" into the geojsons fields and outputting the correct HTML for each individual geojson. So essentially by keeping things static we can parse the HTML into working maps pretty easily and reliably. 

The 3 modules include:
* [pipegeohash](https://github.com/murphy214/pipegeohash) - A table operation for geohashing then a groupby operation at the end (useful for a lot of algorithms and clustering)
* [pipegeojson](https://github.com/murphy214/pipegeojson) - A csv/list/dataframe to geojson parser that uses the assumptions listed above to allow styling from fields in a dataframe column
* [pipehtml](https://github.com/murphy214/pipehtml) - A module that parses the html/JavaScript for all given geojson locations peaking into the geojson to style the pop-up icon in a manner I generally desire

#### Setup and Usage Notes
To setup currently download this repository navigate to it and enter the following in terminal:
```
python setup.py install
```
Prereqs include:
* [geohash](https://github.com/hkwi/python-geohash) (which I think requires XCode this isn't my module just the one I used for the pipegeohash module)
* pandas/numpy

##### Usage Notes
To use berrl the way its currently implemented I recommend using Safari due to being the easiest to use local http references and on the safari bar navigate to "Develop>Disable Local File Restrictions" to allow for local file references. 

As you might have guessed this means you will have to setup a local http server which luckily isn't hard just navigate to the correct directory in terminal that you will be executing your script in and start the HTTP server with the following command in terminal:
```
python -m SimpleHTTPServer
```

Then you should be ready to Map!

#### Simple Example of berrl
Below shows an example of berrl thats is about as simple as I can make it taking a csv file of shark attacks and turning it into geojson parsing and loading the appropriate HTML

```python
import berrl as bl

apikey='your api key'

a=bl.make_points('sharks.csv')
bl.parselist(a,'sharks.geojson') # simply writes a list of lines to file name location

bl.loadparsehtml(['sharks.geojson'],apikey)
```

##### Output of Map Below
![](https://cloud.githubusercontent.com/assets/10904982/13198501/0da25ffe-d7d8-11e5-870c-ebef73bdfd1d.png)

#### A little more Advanced Example
Say we want to iterate through all unique values in a field and style them a certain way based on each unique value in said field. We also only want the most dense areas of shark attacks to map and also want to display the squares in which these densities reside. We could do this pretty easily using berrl. 

**NOTE: that unique values outnumbered unique colors (at least currently) so not all activities were iterated through this is mainly just an example of what you could do.**

```python
import berrl as bl
import pandas as pd
import numpy as np
import itertools

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
```

##### Output Map Below
![](https://cloud.githubusercontent.com/assets/10904982/13198831/795c37a2-d7e1-11e5-9733-584f3f544831.png)
![](https://cloud.githubusercontent.com/assets/10904982/13198832/7c66f176-d7e1-11e5-986d-0da285c97cc1.png)
