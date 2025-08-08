from connect_db import client
from langchain_groq import ChatGroq
from langchain.schema.messages import HumanMessage

def get_student_details(student_id: int) -> str:  
    # Implement the logic to retrieve student details from the database
    student_details = {}
    db = client["ai_education"]
    collection = db["student_data"]
    doc =collection.find_one({"student_id": int(student_id)})
    if doc:
        student_details = {
            "student_id": doc["student_id"],
            "first_name": doc["f_name"],
            "last_name": doc["l_name"],
        }
    
    grades = []
    collection_scores = db["mcq_scores"]
    docs = list(collection_scores.find({"student_id": int(student_id)}))
    overall_score = 0
    i = 0
    for doc in docs:
        i += 1
        overall_score += doc['score']
        grades.append(f"Test ID: {doc['test_id']}, Score: {doc['score']} percent")

    # Optionally, you can include the overall score in the output
    grades.append(f"Overall Score: {overall_score/i if i > 0 else 0}")

    llm2 = ChatGroq(
        model_name="llama-3.3-70b-versatile",  # or llama3-8b-8192 / gemma-7b-it
        api_key="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"
    )

    prompt = f"""
    Genearate a concise summary of the following student details and grades:
    Student Details: {student_details}
    Grades: {grades}
    The summary should be concise and capture the main points.
    The summary should be suitable for a professor reviewing the student's performance.
    seeing the scores comments the student's performance.
    Return output only as text without any additional text.
    """

    response = llm2.invoke(prompt)

    return response.content