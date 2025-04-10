use('mongodbVSCodePlaygroundDB');

db.results.insertMany([
    { result_text: "happy" },
    { result_text: "sad" },
    { result_text: "surprised" }
]);

print("Inserted sample data into the emotion_db database.");
