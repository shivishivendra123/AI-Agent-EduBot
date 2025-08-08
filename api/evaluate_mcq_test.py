from connect_db import client
def evaluate_mcq_test(test_id: str) -> str:
    # Logic to evaluate the MCQ test and generate a report
    db = client["ai_education"]
    submissions_collection = db["mcqs_submissions"]
    tests_collection = db["mcqs"]
    mcq_score_collection = db["mcq_scores"]

    res = mcq_score_collection.find_one({"test_id": str(test_id)})
    if res:
        return f"http://localhost:5173/evaluation_report/{test_id}"
    
    try:
        print(f"Fetching submissions for test_id: {test_id}")
        submission = list(submissions_collection.find({"test_id": str(test_id)}))
    except Exception as e:
        print(f"Error fetching submissions: {e}")
        return "Error fetching submissions."

    if not submission:
        return "No submission found for the given test ID."

    test = tests_collection.find_one({"file_id": str(test_id)})
    if not test:
        return "No test found for the given test ID."
    # mcqs = test["mcqs"]
    # selected_options = submission["selected_options"]   
    # score = 0

    print(test_id)

    report = []

    for sub in submission:
        score = 0
        selected_options = sub["selected_options"]
        for i in range(len(test['mcqs'])):
            if test['mcqs'][i]['answer'] == selected_options[i]:
                score += 4
            else:
                score += -1
        report.append({
            "student_id": sub["student_id"],
            "test_id": sub["test_id"],
            "score": score/20 * 100  # Assuming total score is 20 
        })
    #

    
    
    for r in report:
        mcq_score_collection.insert_one(r)
    
    print(report)

    # print(test['mcqs'])

    # print(submission)
    # print(mcqs)
    

    return f"http://localhost:5173/evaluation_report/{test_id}"
