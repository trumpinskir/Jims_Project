import csv
import pandas as pd
import pprint as p

reader = pd.read_csv('gdax_10_28_2017.csv',delimiter='?')
p.pprint(reader)