# mongoConnection.py connects with MongoDB and sets the functions to insert and call data

from pymongo import MongoClient

client = MongoClient()
db = client.starwars.quotes

def insert(data):
    '''
    This function inserts data into the database 
    Takes: a dictionary with the fields to insert into the DB
    Returns: the object ID
    '''
    res = db.insert_one(data)
    return res.inserted_id


def read(query, project=None):
    '''
    This function reads information from the database 
    Takes: queries and project(Set in None as default) to filter the queries
    Returns: the list with the requested data
    '''
    data = db.find(query, project)
    return list(data)
