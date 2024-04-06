import json
from pymongo import MongoClient
import logging
import argparse

logging.basicConfig(level=logging.INFO)

def import_json_lines(file_path, mongo_uri, db_name, collection_name):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    with open(file_path, 'r', encoding='UTF-8') as file:
        for line in file:
            try:
                document = json.loads(line)
                result = collection.insert_one(document)
                logging.info(f"Inserted document with _id: {result.inserted_id}")
            except Exception as e:
                logging.error(f"Error inserting document: {e}")

def parse_arguments():
    parser = argparse.ArgumentParser(description='Import JSON lines file into MongoDB.')
    parser.add_argument('-i', '--input', required=True, help='Input file path for the JSON lines file.')
    parser.add_argument('-u', '--uri', required=True, help='MongoDB URI.')
    parser.add_argument('-db', '--database', required=True, help='Database name.')
    parser.add_argument('-c', '--collection', required=True, help='Collection name.')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    file_path = args.input
    mongo_uri = args.uri
    db_name = args.database
    collection_name = args.collection

    import_json_lines(file_path, mongo_uri, db_name, collection_name)
