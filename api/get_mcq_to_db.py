import base64
import os
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
from pydantic import BaseModel
from pathlib import Path
from connect_db import client

    
from langchain_groq import ChatGroq
from langchain.schema.messages import HumanMessage

# llm = ChatGroq(
#     api_key="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",
#     model_name="meta-llama/llama-4-maverick-17b-128e-instruct"
# )


#@tool(description="Extract text from a folder containing images. Input: images file path . Output: temp file name where extracted text is saved.")
def get_mcq_from_db(data: str) -> str:
    db = client["ai_education"]
    collection = db["mcqs"]
    my_tests = []

    mcq_submission = db["mcqs_submissions"]
    try:
        all_docs = list(collection.find())
        for doc in all_docs:
            mcq_submission_ = mcq_submission.find_one({"test_id": doc["file_id"]})
            if not mcq_submission_:
                test = f'http://localhost:5173/test/{doc["file_id"]}'.replace("'", "")
                my_tests.append(test)

        return my_tests
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }