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

def encode_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
from langchain_groq import ChatGroq
from langchain.schema.messages import HumanMessage

llm = ChatGroq(
    api_key="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",
    model_name="meta-llama/llama-4-maverick-17b-128e-instruct"
)


@tool(description="Extract text from a folder containing images. Input: images file path . Output: temp file name where extracted text is saved.")
def text_extractor_tool(image_file_path:str) -> str:
    # """extract text from an image files that in folder with path and store the extracted text in blob_name.txt"""
    text_extracted = ""

    image_file_path = image_file_path.strip("\"'")

    for file in sorted(os.listdir(image_file_path)):
        if file.endswith(".jpeg"):
            print(file)
            image_path = os.path.join(image_file_path, file)

            #image_path = "/Users/shivendragupta/Desktop/AI-Agent-Educational/api/page_1.jpeg"
            image_base64 = encode_image_base64(image_path)



            msg = HumanMessage(content=[
                {"type": "text", "text": "Extract all text from this image"},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{image_base64}",
                    "detail": "high"
                }}
            ])

            response = llm([msg])
            text_extracted += response.content + "\n"+"--------------------------------------------------"
    


    path = Path(image_file_path)
    blob_name = path.name


    with open(f"{blob_name}.txt", "w") as file:
        file.write(text_extracted)

    output_path = os.path.abspath(f"{blob_name}.txt")
    print(f"Text extracted and saved to {output_path}")
    return output_path
    # response = llm2.invoke(prompt)

