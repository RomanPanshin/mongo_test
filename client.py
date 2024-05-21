import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

class MongoClientWrapper:
    def __init__(self, connection_string, db_name):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]

    def display_all_documents(self, collection_name):
        """Display all documents in the specified collection"""
        collection = self.db[collection_name]
        documents = collection.find()
        return [self.convert_object_ids(doc) for doc in documents]

    def add_document(self, collection_name, document):
        """Add a document to the specified collection"""
        collection = self.db[collection_name]
        result = collection.insert_one(document)
        return str(result.inserted_id)

    def delete_document(self, collection_name, document_id):
        """Delete a document from the specified collection by _id"""
        collection = self.db[collection_name]
        try:
            result = collection.delete_one({"_id": ObjectId(document_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False

    def search_documents(self, collection_name, criteria):
        """Search for documents in the specified collection by criteria"""
        collection = self.db[collection_name]
        documents = collection.find(criteria)
        return [self.convert_object_ids(doc) for doc in documents]

    def sort_documents(self, collection_name, sort_field, sort_order=pymongo.ASCENDING):
        """Sort documents in the specified collection by a specified field and order"""
        collection = self.db[collection_name]
        documents = collection.find().sort(sort_field, sort_order)
        return [self.convert_object_ids(doc) for doc in documents]

    def convert_object_ids(self, document):
        """Recursively convert ObjectId fields to strings for display"""
        if isinstance(document, dict):
            return {k: self.convert_object_ids(v) for k, v in document.items()}
        elif isinstance(document, list):
            return [self.convert_object_ids(v) for v in document]
        elif isinstance(document, ObjectId):
            return str(document)
        else:
            return document
