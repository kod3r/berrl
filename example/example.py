import berrl as bl

a=bl.make_points('sharks.csv')
bl.parselist(a,'sharks.geojson')

bl.loadparsehtml(['sharks.geojson'])