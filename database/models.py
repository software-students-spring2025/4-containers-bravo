# models.py
from bson.objectid import ObjectId
from db import db

def insert_result(result_text):
    """
    Insert a new emotion analysis result into the database.
    :param result_text: The text result (e.g., the determined emotion).
    :return: The string representation of the inserted document's ObjectId.
    """
    document = {
        "result_text": result_text
    }
    result = db.results.insert_one(document)
    return str(result.inserted_id)

def get_result(result_id):
    """
    Retrieve a result from the database using its id.
    :param result_id: The string form of the ObjectId.
    :return: The result document, or None if not found.
    """
    document = db.results.find_one({"_id": ObjectId(result_id)})
    if document:
        document['_id'] = str(document['_id'])
    return document

def get_all_results():
    """
    Retrieve all results stored in the database.
    :return: A list of result documents with ObjectIds as strings.
    """
    results = list(db.results.find())
    for doc in results:
        doc['_id'] = str(doc['_id'])
    return results
