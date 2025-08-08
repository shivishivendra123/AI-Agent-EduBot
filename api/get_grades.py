from connect_db import client
def get_grades(data=None) -> list:
    # Implement the logic to retrieve grades from the database
    grades = []
    db = client["ai_education"]
    collection = db["mcq_scores"]
    docs =list(collection.find({"student_id": 2}))
    overall_score = 0
    i = 0
    for doc in docs:
        i += 1
        overall_score += doc['score']
        grades.append(f"Test ID: {doc['test_id']}, Score: {doc['score']} percent")

    # Optionally, you can include the overall score in the output
    grades.append(f"Overall Score: {overall_score/i if i > 0 else 0}")

    return grades
