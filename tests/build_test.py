# unit tests for each of the 3 main modules within berrl
import os

#testing pipegeohash
os.chdir('pipegeohash_test')
execfile('test_pipegeohash.py')
os.chdir('..')

# testing pipegeojson
os.chdir('pipegeojson_test')
execfile('test_pipegeojson.py')
os.chdir('..')
