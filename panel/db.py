import pymongo
import time


def db_init(collection=None):
    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        print("Connected to MongoDB successfully!")
    except pymongo.errors.ConnectionFailure as e:
        print("Failed to connect to MongoDB. Error:", str(e))
        raise
    myclient = pymongo.MongoClient("mongodb://localhost:27017")
    mydb = myclient["rahneshan"]
    if collection ==None:
        mycol = mydb["users"]
    else:
        mycol = mydb[collection]
    return mycol

def get_user(username,password):
    mycol = db_init('users')
    query = {'$and':[{'phone': username,'password': password}]}
    data = list(mycol.find(query))
    return data


def get_setting():
    mycol = db_init('setting')
    query = {'type': 'main'}
    data = list(mycol.find(query))
    return data[0]

def update_last_update():
    mycol = db_init('setting')
    query = {'type': 'main'}
    newvalues = { "$set": { "last_update": int(time.time()) } }
    mycol.update_one(query, newvalues)


def get_packages(operator=None):
    if operator !=None:
        query = {'operator':operator}
    else:
        query = {}
    mycol = db_init('packages')
    data = list(mycol.find(query))
    return data

def get_requests(user):
    query = {'user':user}
    mycol = db_init('requests')
    data = list(mycol.find(query))
    return data

def insert_requests(request):
    mycol = db_init('requests')
    mycol.insert_one(request)

def update_reqest_feedback(id,feedback):
    mycol = db_init('requests')
    query = {'_id': id}
    myset = {'$set':{'feedback': feedback}}
    mycol.update_one(query,myset)
    
