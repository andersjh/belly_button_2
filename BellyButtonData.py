# dependencies
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, join, outerjoin, MetaData, Table

from config import connect_string

class BellyButtonData():

    def __init__(self):
        self.engine = create_engine(connect_string)
        # self.conn = self.engine.connect()
        self.connect_string = connect_string
        self.inspector = inspect(self.engine)
        self.tables = self.inspector.get_table_names()
        self.Base = automap_base()
        self.Base.prepare(self.engine, reflect=True)
        self.Subjects = self.Base.classes['subjects']
        self.meta = MetaData()
        self.TestResults = Table('test_results_view', self.meta, 
                    autoload_with=self.engine)


    def display_db_info(self):
        inspector = inspect(self.engine)
        tables = self.inspector.get_table_names()
        for table in self.tables:
            print("\n")
            print('-' * 12)
            print(f"table '{table}' has the following columns:")
            print('-' * 12)
            for column in self.inspector.get_columns(table):
                print(f"name: {column['name']}   column type: {column['type']}")


    def get_subject_ids(self):
        session = Session(self.engine)

        results = session.query(self.Subjects.id)
            
        df = pd.read_sql(results.statement, session.connection())

        session.close()  
        return list(df.id)  


    def get_subjects(self, subj_id=0):
        session = Session(self.engine)

        if subj_id == 0:
            results = session.query(self.Subjects)
        else:
            results = session.query(self.Subjects).filter(self.Subjects.id == subj_id)    
            
        df = pd.read_sql(results.statement, session.connection())

        session.close()  
        return df.to_dict(orient="records")     

    def get_test_results(self, subj_id=0): 
        session = Session(self.engine)

        if subj_id == 0:
            results = session.query(self.TestResults)
        else:
            results = session.query(self.TestResults).filter_by(subject_id = subj_id)    
            
        df = pd.read_sql(results.statement, session.connection())
        df = df.sort_values(by='amount', ascending=False)

        session.close()  
        return df.to_dict(orient="records")    

    def get_data_by_user(self, subj_id=940):
        return {
            '_id': subj_id,
            'user': self.get_subjects(subj_id)[0],
            'results': self.get_test_results(subj_id)
        }     

    def get_data_for_all(self):
        total_data = []
        subjects = self.get_subjects()
        num_records = len(subjects)
        for i in range(num_records):
            cur_subj = subjects[i]['id']
            total_data.append({
                '_id': cur_subj,
                'user': subjects[i],
                'results': self.get_test_results(cur_subj)                
            })
        return total_data    



if __name__ == '__main__':
    info = BellyButtonData()
    info.display_db_info()
    print("\nSubject IDs\n", info.get_subject_ids())
    print("\nsubject 1286:\n", info.get_subjects(1286))
    print("\nResults 1286:\n", info.get_test_results(1286))
    print("\nData for user 1286:\n", info.get_data_by_user(1286))



        