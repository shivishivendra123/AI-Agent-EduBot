from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from langchain_core.tools import BaseTool
from langchain_core.tools import tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

from langchain_groq import ChatGroq

# @tool
def generate_mcq_test(temp_file_name: str) -> str:

    clean_path = temp_file_name.strip("\"'")

    with open(clean_path, 'r', encoding='utf-8') as file:
        extracted_text = file.read()

    print(extracted_text)

    llm2 = ChatGroq(
                    model_name="llama-3.3-70b-versatile",  # or llama3-8b-8192 / gemma-7b-it
                    api_key="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"
                )



    prompt = f"""
You are a chemistry teacher preparing multiple-choice questions (MCQs) for a high school exam.
Your task is to generate concept-based MCQs from the following textbook passage.

Only ask questions that check understanding of the topic. Do NOT ask about process steps or formats.

Text:
\"\"\"
{extracted_text}
\"\"\"

Generate 5 MCQs. Each question should have 4 options (a-d) and one correct answer.
Return the result in the following JSON format:

[
  {{
    "question": "...",
    "option_a": "...",
    "option_b": "...",
    "option_c": "...",
    "option_d": "...",
    "answer": "option_x"
  }},
  ...
]

dont add any additional text or explanation, just return the JSON array.
"""

    response = llm2.invoke(prompt)

    with open("output_pdf.txt", "w") as file:
        file.write(response.content)

    return response.content
