print('> Trying To Connect To Database...')
import pymongo
import sys, time

try:
  myclient = pymongo.MongoClient('mongodb+srv://techz:wall@techzwallbotdb.katsq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
  queuedb = myclient["animedex"]["queue"]
  tempdb = myclient["animedex"]["tempdb"]
except Exception as e:
  print('> Failed To Connect To Database... Check Your Internet Connection\n',e)
  time.sleep(10)
  sys.exit()

def is_inBlogger(name):
  data = queuedb.find_one({"name": name})
  if data:
      return True
  return False

def save_inBlogger(name): 
  data = queuedb.insert_one({"name": name})
  return

def is_inDB(name):
  data = tempdb.find_one({"name": name})

  if data:
      return True
  return False

def save_inDB(name): 
  data = tempdb.insert_one({"name": name})
  return

def del_inDB(name): 
  data = tempdb.delete_one({"name": name})
  return

def get_all():
  all1 = tempdb.find({})
  return all1

print('> Connected Succesfully')