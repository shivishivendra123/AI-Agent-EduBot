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
from fpdf import FPDF
from upload_utility import upload_to_gcs
import uuid

def sanitize_text(text: str) -> str:
    return text.encode("latin-1", "ignore").decode("latin-1")

def encode_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
from langchain_groq import ChatGroq
from langchain.schema.messages import HumanMessage

@tool(description="Generate a summary in PDF format from extracted text from file: Input: temp file name where extracted text is saved. Output: url of saved summary on cloud")
def save_summary_to_pdf(temp_file_name: str) -> str:

    clean_path = temp_file_name.strip("\"'")

    with open(clean_path, 'r', encoding='utf-8') as file:
        extracted_text = file.read()

    llm2 = ChatGroq(
        model_name="llama-3.3-70b-versatile",  # or llama3-8b-8192 / gemma-7b-it
        api_key="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"
    )

    prompt = f"""
    Generate a summary of the following text:
    The summary should be concise and capture the main points.
    The summary should be scientific in nature.
    The summary should be suitable for a student studying the content.
    The summary should be detailed and informative.
    \"\"\"{extracted_text}\"\"\"
    Return output only as text without any additional text.
    """

    response = llm2.invoke(prompt)

    with open("summary.txt", "w") as file:
        file.write(response.content)

    


    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in response.content.split('\n'):

        pdf.multi_cell(0, 10, sanitize_text(line))
    pdf.output("summary.pdf")

    random_gid = str(uuid.uuid4())

    upload_to_gcs(source_file_path='/Users/shivendragupta/Desktop/AI-Agent-Educational/api/summary.pdf', destination_blob_name=f'course_material/{random_gid}')
    print(f"Summary saved to summary.pdf")

    url = f"https://storage.googleapis.com/assignment_agent/course_material/{random_gid}"

    return {
        'url':url
    }