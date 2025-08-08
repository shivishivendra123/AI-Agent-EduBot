from fastapi import FastAPI
from fastapi import UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from queue import Queue
from upload_utility import upload_to_gcs
import uuid
from pydantic import BaseModel
from agent_config import agent_executor
from connect_db import client
from get_course_announcements import get_course_announcements
from create_course_annoucements import create_course_announcements

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with ["http://localhost:5173"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

queue_uploaded = Queue()
UPLOAD_DIR = '/Users/shivendragupta/Desktop/AI-Agent-Educational/uploads/files'

@app.post("/uploadFile")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Add the file to the queue
    queue_uploaded.put(file_path)
    print(queue_uploaded.queue)
    # Upload the file to Google Cloud Storage
    random_gid = str(uuid.uuid4())
    upload_to_gcs(source_file_path=file_path, destination_blob_name=random_gid)
    
    return {"filename": file.filename, "path": file_path , "file_gid":random_gid}

@app.get("/getUploadedFiles")
async def get_uploaded_files_from_queue():
    if not queue_uploaded.empty():
        file_path = queue_uploaded.get()
        print(queue_uploaded.queue)
        return {"file_path": file_path}
    else:
        return JSONResponse(status_code=404, content={"message": "No files in the queue"})

class Conversation_data(BaseModel):
    conversation_id:str
    file_id: str
    prompt: str



@app.post('/conversation')
def conversation(data: Conversation_data):
    result = None
    if(data.file_id is None or data.file_id.strip() == ""):
        result = agent_executor.invoke({"input": f"{data.prompt}"})
    else:
        result = agent_executor.invoke({"input": f"{data.prompt} from blob_name {data.file_id}"})

    # Print result
    return result


@app.post('/conversation_student')
def conversation_student(data: Conversation_data):
    result = agent_executor.invoke({"input": f"{data.prompt}"})
    return result

@app.get('/get_my_tests/{id}')
def get_my_tests(id: str):
    # Logic to retrieve and return the tests for the user

    db = client["ai_education"]
    collection = db["mcqs"]

    # Query example: find documents where "file_id" is "active"
    query = {"file_id": id}

    results = collection.find(query)

    res = []
    for doc in results:
        res.append(doc["mcqs"])



    return {"results": res}

class SubmitMCQTest(BaseModel):
    test_id: str
    selected_options: list[str]
    student_id: int

@app.post('/submit_mcq_test')
def submit_mcq_test(data: SubmitMCQTest):

    db = client["ai_education"]
    collection = db["mcqs_submissions"]

    existing_submission = collection.find_one({"test_id": data.test_id, "student_id": data.student_id})
    # If a submission already exists, return an error message
    if existing_submission:
        return {"message": "You have already submitted this test."}

    # Insert the submitted test data into the database
    collection.insert_one(data.dict())



    return {
        "message": "Test submitted successfully!",
        "test_id": data.test_id,
        "selected_options": data.selected_options,
        "student_id": data.student_id
    }

@app.get('/get_mcq_tests_report/{test_id}')
def get_mcq_tests_report(test_id: str):
    print(test_id)  
    # Logic to retrieve and return the evaluation report for the given test ID
    db = client["ai_education"]
    collection = db["mcq_scores"]

    report = list(collection.find({"test_id": str(test_id)}))
    # if not report:
    #     return {"message": "No report found for the given test ID."}

    result = []
    for r in report:
        result.append({
            "student_id": r["student_id"],
            "score": r["score"]
        })

    return {"report": result}

@app.get('/check_test_availability/{url}')
def check_test_availability(url: str):      
    db = client["ai_education"]
    collection = db["mcqs_submissions"]
    print(url)
    test = collection.find_one({"test_id": url})
    if test:
        return {"available": True}
    else:
        return {"available": False}
    
@app.get('/get_unevaluated_tests')
def get_unevaluated_tests():

    db = client["ai_education"]
    collection = db["mcqs"]
    my_tests = []

    mcq_submission = db["mcqs_submissions"]
    try:
        all_docs = list(collection.find())
        for doc in all_docs:
            mcq_submission_ = mcq_submission.find_one({"test_id": doc["file_id"]})
            if not mcq_submission_:
                test = doc["file_id"]
                my_tests.append(test)

        return my_tests
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.get('/get_evaluated_tests')
def get_evaluated_tests():

    db = client["ai_education"]
    collection = db["mcqs"]
    my_tests = []

    mcq_submission = db["mcqs_submissions"]
    try:
        all_docs = list(collection.find())
        for doc in all_docs:
            mcq_submission_ = mcq_submission.find_one({"test_id": doc["file_id"]})
            if mcq_submission_:
                test = doc["file_id"]
                my_tests.append(test)

        return my_tests
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }