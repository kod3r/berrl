import berrl as bl

# please, if possible, don't abuse this key its not difficult to get your own
apikey='your api key'

a=bl.make_points('sharks.csv')
bl.parselist(a,'sharks.geojson') # simply writes a list of lines to file name location

bl.loadparsehtml(['sharks.geojson'],apikey)
