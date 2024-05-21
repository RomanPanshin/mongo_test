import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB connection string
connection_string = "mongodb://root:example@localhost:27017/?authSource=admin"

# Connect to MongoDB
client = MongoClient(connection_string)

# Access the database
db = client.sweets_db

def display_all_documents(collection_name):
    """Display all documents in the specified collection"""
    collection = db[collection_name]
    documents = collection.find()
    for doc in documents:
        print(doc)

def add_document(collection_name, document):
    """Add a document to the specified collection"""
    collection = db[collection_name]
    collection.insert_one(document)
    print("Document added successfully")

def delete_document(collection_name, document_id):
    """Delete a document from the specified collection by _id"""
    collection = db[collection_name]
    result = collection.delete_one({"_id": ObjectId(document_id)})
    if result.deleted_count > 0:
        print("Document deleted successfully")
    else:
        print("No document found with the specified _id")

def search_documents(collection_name, criteria):
    """Search for documents in the specified collection by criteria"""
    collection = db[collection_name]
    documents = collection.find(criteria)
    for doc in documents:
        print(doc)

def sort_documents(collection_name, sort_field, sort_order=pymongo.ASCENDING):
    """Sort documents in the specified collection by a specified field and order"""
    collection = db[collection_name]
    documents = collection.find().sort(sort_field, sort_order)
    for doc in documents:
        print(doc)

# Test the functions
if __name__ == "__main__":
    collection_name = 'products'  # Change this to the collection you want to work with

    print("Displaying all documents:")
    display_all_documents(collection_name)
    
    print("\nAdding a new document:")
    new_document = {
        "name": "Marshmallow",
        "description": "Soft and fluffy marshmallow",
        "price": 1.0,
        "category_id": db.categories.find_one({ "name": "Candy" }).get("_id"),
        "production_detail_id": db.productionDetails.insert_one({
            "production_date": "2024-05-01",
            "expiration_date": "2025-05-01",
            "batch_number": "D101"
        }).inserted_id
    }
    add_document(collection_name, new_document)
    
    print("\nDisplaying all documents:")
    display_all_documents(collection_name)
    
    print("\nDeleting a document by _id:")
    document_id_to_delete = input("Enter the _id of the document to delete: ")
    delete_document(collection_name, document_id_to_delete)
    
    print("\nDisplaying all documents:")
    display_all_documents(collection_name)
    
    print("\nSearching for documents by name:")
    search_criteria = { "name": "Gummy Bears" }
    search_documents(collection_name, search_criteria)
    
    print("\nSorting documents by price in ascending order:")
    sort_documents(collection_name, "price", pymongo.ASCENDING)
    
    print("\nSorting documents by price in descending order:")
    sort_documents(collection_name, "price", pymongo.DESCENDING)
