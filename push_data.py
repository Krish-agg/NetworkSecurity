import os
import sys
import json
import certifi
import pandas as pd
import numpy as np
import pymongo
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging  

from dotenv import load_dotenv

load_dotenv()
MONGO_DB_URL = os.getenv('MONGO_DB_ATLAS_URL')

ca=certifi.where()

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

    def csvToJson(self, file_path: str) -> list:
        """
        Converts a CSV file to a list of dictionaries.
        
        :param file_path: Path to the CSV file.
        :return: List of dictionaries representing the CSV data.
        """
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True, inplace=True)
            data = json.loads(df.to_json(orient='records'))
            return data
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def pushDataToMongoDB(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records = records
            self.mongodb_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongodb_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            logging.info(f"Data pushed to MongoDB collection: {self.collection}")
            return (len(self.records))

        except Exception as e:
            raise NetworkSecurityException(e, sys)
 

if __name__ == "__main__":
    FILE_PATH = 'Network_Data\phisingData.csv'
    DATABASE='NetworkSecurityML'
    COLLECTION='phishingData'
    network_data_extractor = NetworkDataExtract()
    records=network_data_extractor.csvToJson(FILE_PATH)
    noRecords= network_data_extractor.pushDataToMongoDB(records, DATABASE, COLLECTION)
    print(f"Number of records pushed to MongoDB: {noRecords}")
    