from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client['musiclibrary']  # Replace with your database name

# Select the collection to delete from
collection_name = 'albums'  # Replace with your collection name
collection = db[collection_name]

try:
    # Delete all documents in the collection
    delete_result = collection.delete_many({})

    # Print confirmation message
    print(f"Deleted {delete_result.deleted_count} documents from the collection '{collection_name}'")

except Exception as e:
    print(f"Error deleting documents from collection '{collection_name}': {str(e)}")

finally:
    # Close MongoDB client connection
    client.close()