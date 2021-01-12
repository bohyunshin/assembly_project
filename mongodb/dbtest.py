from pymongo import MongoClient
import pandas as pd

my_client = MongoClient('mongodb://127.0.0.1:27017/')


mydb = my_client['test']
mycol = mydb['customers']

# x = mycol.insert_one({'name':'hi', 'address':'assembly'})

x = mycol.find_one()
print(x)