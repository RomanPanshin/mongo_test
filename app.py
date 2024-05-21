from flask import Flask, render_template, request, redirect, url_for, jsonify
from client import MongoClientWrapper
import pymongo

app = Flask(__name__)

# MongoDB connection string and database name
connection_string = "mongodb://root:example@localhost:27017/?authSource=admin"
db_name = "sweets_db"

# Initialize MongoClientWrapper
mongo_client = MongoClientWrapper(connection_string, db_name)

@app.route('/')
def main():
    tables = ['products', 'categories', 'productionDetails', 'ingredients', 'suppliers']
    return render_template('main.html', tables=tables)

@app.route('/table/<collection_name>')
def table(collection_name):
    sort_field = request.args.get('field')
    sort_order = request.args.get('order', 'asc')
    search_key = request.args.get('search_key')
    search_value = request.args.get('search_value')
    
    if search_key and search_value:
        criteria = {search_key: search_value}
        documents = mongo_client.search_documents(collection_name, criteria)
    elif sort_field:
        sort_order = pymongo.ASCENDING if sort_order == 'asc' else pymongo.DESCENDING
        documents = mongo_client.sort_documents(collection_name, sort_field, sort_order)
    else:
        documents = mongo_client.display_all_documents(collection_name)
    
    return render_template('table.html', collection_name=collection_name, documents=documents)

@app.route('/add/<collection_name>', methods=['GET', 'POST'])
def add_document(collection_name):
    if request.method == 'POST':
        document = request.form.to_dict()
        inserted_id = mongo_client.add_document(collection_name, document)
        return redirect(url_for('table', collection_name=collection_name))
    return render_template('add_document.html', collection_name=collection_name)

@app.route('/delete/<collection_name>/<document_id>', methods=['POST'])
def delete_document(collection_name, document_id):
    success = mongo_client.delete_document(collection_name, document_id)
    return redirect(url_for('table', collection_name=collection_name))

if __name__ == '__main__':
    app.run(debug=True)
