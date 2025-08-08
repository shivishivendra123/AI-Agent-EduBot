from langchain_core.tools import BaseTool
from langchain_core.tools import tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
import io
from google.cloud import storage
from urllib.parse import urlparse
import fitz  # PyMuPDF
import os

@tool(description="Load file from gcs and Extract JPEG images from a PDF file. Input: PDF file stream. Output: blob_name")
def pdf_to_text_extractor_tool(blob_name:str) -> str:
    blob_name = blob_name.strip().strip("'").strip('"')
    client = storage.Client()
    bucket = client.bucket("assignment_agent")
    blob = bucket.blob(blob_name)
    
    pdf_bytes = blob.download_as_bytes()
    pdf_stream = io.BytesIO(pdf_bytes)

    doc = fitz.open(stream = pdf_stream,  filetype="pdf")

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=300)
        output_dir = f"/Users/shivendragupta/Desktop/AI-Agent-Educational/{blob_name}"
        os.makedirs(output_dir, exist_ok=True)
        output = f"/Users/shivendragupta/Desktop/AI-Agent-Educational/{blob_name}/page_{page_num + 1}.jpeg"
        pix.save(output)
    
    return f"files saved as JPEGs in folder /Users/shivendragupta/Desktop/AI-Agent-Educational/{blob_name}"


