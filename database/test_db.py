import unittest
from models import insert_result, get_result, get_all_results
from db import db

class TestDB(unittest.TestCase):
    
    def setUp(self):
        # Clear the "results" collection before each test.
        db.results.delete_many({})

    def test_insert_and_get_result(self):
        text = "happy"
        result_id = insert_result(text)
        retrieved = get_result(result_id)
        self.assertEqual(retrieved["result_text"], text)

    def test_get_all_results(self):
        texts = ["happy", "sad", "excited"]
        for t in texts:
            insert_result(t)
        results = get_all_results()
        self.assertEqual(len(results), len(texts))
        result_texts = [doc["result_text"] for doc in results]
        self.assertCountEqual(result_texts, texts)

if __name__ == '__main__':
    unittest.main()
