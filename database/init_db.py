from db import db

def init_db():
    # Create an index on "result_text" if you expect to query by it frequently.
    # (Alternatively, if you add more fields, you can adjust indexes accordingly.)
    db.results.create_index("result_text")
    print("Database initialized with indexes.")

if __name__ == "__main__":
    init_db()
