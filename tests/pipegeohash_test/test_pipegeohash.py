# testing the output of the pipegeohash module against competing input methods
import berrl as bl
import itertools

# inputing a csv file location for test
hashedtable1=bl.map_table('sharks.csv',5)

# reading output csv table to memory as it will be overwritten in the next test
squaretable1=bl.read('squares5.csv')

#inputing a list for test 
#first reading list to memory
testlist=bl.read('sharks.csv')
hashedtable2=bl.map_table(testlist,5,list=True)

# reading output csv table to memory as it will be overwritten in the next test
squaretable2=bl.read('squares5.csv')

# testing each square table against each other
ind=0
for a,b in itertools.izip(squaretable1,squaretable2):
	if not a==b:
		ind=1

# carrying the passing of square status down to the test for the hashed table test
if ind==0:
	passing=0
else:
	passing=1

# testing each hashed table against each other
ind=0
for a,b in itertools.izip(hashedtable1,hashedtable2):
	if not a==b:
		ind=1

# carrying the passing of square status down to the test for the hashed table test
if ind==0 and passing==0:
	passing=0
else:
	passing=1

# printing output result
if passing==0:
	print 'pipegeohash build passed'
else:
	print 'pipegeohash build failed'