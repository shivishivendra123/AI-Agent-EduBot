import base64
import re
import json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from pydoc import text
from langchain_core.tools import BaseTool
from langchain_core.tools import tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from fpdf import FPDF

from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from connect_db import client

import json



class MCQ(BaseModel):
    question: str
    options: List[str]
    answer: str

class MCQDocument(BaseModel):
    file_id: str
    mcqs: List[MCQ]


def save_mcq_to_db(temp_file_name: str):

    path = f"{temp_file_name}.txt"

    clean_path = path.strip("\"'")

    with open("output_pdf.txt", 'r', encoding='utf-8') as file:
        extracted_text = file.read()

    payload = json.loads(extracted_text)

    document = {
        "file_id": temp_file_name,
        "mcqs": payload,
        "created_at": datetime.utcnow()
    }
    db = client["ai_education"]
    collection = db["mcqs"]
    try:
        result = collection.insert_one(document)
        return {"status": "success", "inserted_id": str(result.inserted_id)}
    except Exception as e:
        return {
            "status":"error","message":str(e)
        }