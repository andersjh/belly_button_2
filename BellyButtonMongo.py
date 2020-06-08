# dependencies
import pandas as pd
from pymongo import MongoClient
from config import connect_string

class BellyButtonMongo():

    def __init__(self):
        self.client = MongoClient(connect_string)
        self.db = self.client.bellybutton
        self.test_results = self.db.test_results


    def get_subject_ids(self):
        return [i['_id'] for i in self.test_results.find({}, {"_id":1})]


    def get_subjects(self, subj_id=0):
        if subj_id != 0:
            subj_id = int(subj_id)
            results = [subj_id]
            results = [i['user'] for i in self.test_results.find({"_id": subj_id}, {"user": 1})]
        else:
            results = [i['user'] for i in self.test_results.find({}, {"user": 1})]
            
        return results     

    def get_test_results(self, subj_id=0): 
        if subj_id != 0:
            subj_id = int(subj_id)
            results = [self.test_results.find_one(subj_id, {"results": 1})['results']]
        else:
            results = [i['results'] for i in self.test_results.find({}, {"results": 1})]
            
        return results     
  

    def get_data_by_user(self, subj_id=940):
        subj_id = int(subj_id)
        return self.test_results.find_one(subj_id)

    def get_data_for_all(self):
        return [i for i in self.test_results.find()]



if __name__ == '__main__':
    info = BellyButtonMongo()
    print("\nSubject IDs\n", info.get_subject_ids())
    print("\nsubject 1286:\n", info.get_subjects(1286))
    print("\nResults 1286:\n", info.get_test_results(1286))
    print("\nData for user 1286:\n", info.get_data_by_user(1286))



        