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
from google.cloud import storage
    
from langchain_groq import ChatGroq
from langchain.schema.messages import HumanMessage

# llm = ChatGroq(
#     api_key="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",
#     model_name="meta-llama/llama-4-maverick-17b-128e-instruct"
# )


#@tool(description="Extract text from a folder containing images. Input: images file path . Output: temp file name where extracted text is saved.")
def get_course_material_from_cloud(data: str) -> str:
    client = storage.Client()
    bucket = client.get_bucket('assignment_agent')

    # List all files in the bucket
    list_of_files = []
    # Get all blobs with the given prefix (acts like a folder)
    blobs = bucket.list_blobs(prefix='course_material')

    file_paths = [blob.name for blob in blobs]

    for file_path in file_paths:
        list_of_files.append(f'https://storage.googleapis.com/assignment_agent/{file_path}'.replace("'", ""))

    return list_of_files

