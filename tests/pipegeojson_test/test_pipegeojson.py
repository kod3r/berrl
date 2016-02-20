# testing the output of pipegeojson against different input types
import berrl as bl
import itertools

# making line with csv file location
line1=bl.make_line('csvs/line_example.csv')

# making line with list 
testlist=bl.read('csvs/line_example.csv')
line2=bl.make_line(testlist,list=True)

# testing each line geojson against each other
ind=0
for a,b in itertools.izip(line1,line2):
	if not a==b:
		ind=1

# carrying the passing of status down to the test for the rest
if ind==0:
	passing=0
else:
	passing=1

# making points with csv file location
points1=bl.make_line('csvs/points_example.csv')

# making points with list 
testlist=bl.read('csvs/points_example.csv')
points2=bl.make_line(testlist,list=True)

# testing each points geojson against each other
ind=0
for a,b in itertools.izip(points1,points2):
	if not a==b:
		ind=1

# carrying the passing of status down to the test for the rest
if ind==0 and passing==0:
	passing=0
else:
	passing=1

# making blocks with csv file location
blocks1=bl.make_line('csvs/blocks_example.csv')

# making blocks with list 
testlist=bl.read('csvs/blocks_example.csv')
blocks2=bl.make_line(testlist,list=True)

# testing each bloocks geojson against each other
ind=0
for a,b in itertools.izip(blocks1,blocks2):
	if not a==b:
		ind=1

# carrying the passing of status down to the test for the rest
if ind==0 and passing==0:
	passing=0
else:
	passing=1

# making blocks with csv file location
polygon1=bl.make_line('csvs/polygon_example.csv')

# making blocks with list 
testlist=bl.read('csvs/polygon_example.csv')
polygon2=bl.make_line(testlist,list=True)

# testing each bloocks geojson against each other
ind=0
for a,b in itertools.izip(polygon1,polygon2):
	if not a==b:
		ind=1

# carrying the passing of status down to the test for the rest
if ind==0 and passing==0:
	passing=0
else:
	passing=1

# printing output result
if passing==0:
	print 'pipegeojson build passed'
else:
	print 'pipegeojson build failed'


