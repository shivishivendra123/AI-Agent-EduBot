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
def miscellaneous_tool(data: str) -> str:
    return "Please suggest a valid query related to MCQ tests or other functionalities. If you need help with MCQ tests, please use the appropriate tool to retrieve them from the database."