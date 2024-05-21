#!/bin/bash

# Base URL of the Flask server
BASE_URL="http://127.0.0.1:5000"

# Function to add a document to a specified collection
add_document() {
    local collection_name=$1
    local document=$2
    curl -X POST -H "Content-Type: application/json" -d "$document" "$BASE_URL/documents/$collection_name"
}

# Adding sample data to Categories collection
echo "Adding categories..."
add_document "categories" '{"name": "Chocolate", "description": "Chocolate sweets"}'
add_document "categories" '{"name": "Candy", "description": "Candy sweets"}'

# Adding sample data to Suppliers collection
echo "Adding suppliers..."
add_document "suppliers" '{"name": "Supplier A", "contact_info": "contact@supplierA.com", "address": "123 Supplier St"}'
add_document "suppliers" '{"name": "Supplier B", "contact_info": "contact@supplierB.com", "address": "456 Supplier Ave"}'

# Get the inserted Category and Supplier IDs (You might need to adjust this part based on your setup)
CHOCOLATE_CATEGORY_ID=$(curl -s "$BASE_URL/documents/categories" | jq -r '.[0]._id')
CANDY_CATEGORY_ID=$(curl -s "$BASE_URL/documents/categories" | jq -r '.[1]._id')
SUPPLIER_A_ID=$(curl -s "$BASE_URL/documents/suppliers" | jq -r '.[0]._id')
SUPPLIER_B_ID=$(curl -s "$BASE_URL/documents/suppliers" | jq -r '.[1]._id')

# Adding sample data to Ingredients collection
echo "Adding ingredients..."
add_document "ingredients" "{\"name\": \"Cocoa\", \"supplier_id\": \"$SUPPLIER_A_ID\"}"
add_document "ingredients" "{\"name\": \"Sugar\", \"supplier_id\": \"$SUPPLIER_B_ID\"}"

# Get the inserted Ingredient IDs (You might need to adjust this part based on your setup)
COCOA_ID=$(curl -s "$BASE_URL/documents/ingredients" | jq -r '.[0]._id')
SUGAR_ID=$(curl -s "$BASE_URL/documents/ingredients" | jq -r '.[1]._id')

# Adding sample data to ProductionDetails collection
echo "Adding production details..."
add_document "productionDetails" '{"production_date": "2024-05-01", "expiration_date": "2025-05-01", "batch_number": "A123"}'
add_document "productionDetails" '{"production_date": "2024-06-01", "expiration_date": "2025-06-01", "batch_number": "B456"}'

# Get the inserted ProductionDetail IDs (You might need to adjust this part based on your setup)
PRODUCTION_DETAIL_1_ID=$(curl -s "$BASE_URL/documents/productionDetails" | jq -r '.[0]._id')
PRODUCTION_DETAIL_2_ID=$(curl -s "$BASE_URL/documents/productionDetails" | jq -r '.[1]._id')

# Adding a lot of sample data to Products collection
echo "Adding products..."
for i in {1..100}
do
    add_document "products" "{\"name\": \"Chocolate Bar $i\", \"description\": \"Delicious chocolate bar $i\", \"price\": 2.5, \"category_id\": \"$CHOCOLATE_CATEGORY_ID\", \"production_detail_id\": \"$PRODUCTION_DETAIL_1_ID\"}"
    add_document "products" "{\"name\": \"Candy Cane $i\", \"description\": \"Sweet candy cane $i\", \"price\": 1.0, \"category_id\": \"$CANDY_CATEGORY_ID\", \"production_detail_id\": \"$PRODUCTION_DETAIL_2_ID\"}"
done

echo "Database populated with sample data."

