import berrl as bl
import pandas as pd
import numpy as np

d=pd.read_csv('STSIFARS.csv')
d=d[d.STANAME=='WEST VIRGINIA']
d.to_csv('wv_traffic_fatals.csv')