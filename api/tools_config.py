from langchain.agents import create_react_agent, AgentExecutor, Tool, initialize_agent
from langchain import hub
from load_from_gcs_pdf_to_image import pdf_to_text_extractor_tool
from images_to_text import text_extractor_tool
from text_mcq_test import generate_mcq_test
from summary_to_pdf import save_summary_to_pdf
# from load_file_gcs import load_files_from_gcs
from langchain_groq import ChatGroq
from langchain.globals import set_llm_cache
from save_mcq_to_db import save_mcq_to_db
from get_mcq_to_db import get_mcq_from_db
from get_course_material_from_cloud import get_course_material_from_cloud
from get_course_announcements import get_course_announcements
from create_course_annoucements import create_course_announcements
from upload_course_material_to_cloud import upload_course_material_to_cloud
from evaluate_mcq_test import evaluate_mcq_test
set_llm_cache(None)  # disables caching
from miscellaneous_tool import miscellaneous_tool
from get_grades import get_grades
from get_student_details import get_student_details
tools = [
    Tool(
        name="PDF to Images",
        func=pdf_to_text_extractor_tool,
        description="Load file from gcs and Extract JPEG images from a PDF file. Input: PDF file stream. Output: path to image folder"
    ),
    Tool(
        name="Images to Text",
        func=text_extractor_tool,
        description="Extract text from a folder containing images. Input: images file path . Output: temp file name where extracted text is saved."
    ),
    Tool(
        name="Text to MCQ",
        func=generate_mcq_test,
        description="Generate MCQs in JSON format from extracted text from file . Input: temp file name where extracted text is saved. Output: JSON with MCQs."
    ),
    Tool(
        name="Summary to PDF",
        func=save_summary_to_pdf,
        description="Generate a summary in PDF format from extracted text from file: Input: temp file name where extracted text is saved. Output: url of saved summary on cloud"
    ),
    Tool(
        name='Save MCQS to DB',
        func=save_mcq_to_db,
        description="Save already extracted mcqs from txt file named after blob_name and save to database if the user ask.Input: blob_name .Output: File has been saved in Database"
    ),
    Tool(
        name="Get MCQ Test from DB",
        func = get_mcq_from_db,
        description="Get My MCQ Test. Input: None. Output: MCQ data from DB no extra text or explanation is needed. Just return the MCQ data in array",
    ),
    Tool(
        name="If Query is not related to any of the above tools",
        func = miscellaneous_tool,
        description="Handle queries that do not match any specific tool. Input: User query. Output: Appropriate response or action.",
    ),
    Tool(
        name="Get course material from cloud",
        func=get_course_material_from_cloud,
        description="Get my course material. Input: None. Output: Course material data  no extra text or explanation is needed. Just return the course material data in array.",
    ),
    Tool(
        name="Get Course Announcements",
        func=get_course_announcements,
        description="Get my course announcements. Input: None. Output: Course announcements data no extra text or explanation is needed. Just return the course announcements data in array."
    ),
    Tool(
        name="Create Course Announcements",
        func=create_course_announcements,
        description="Create a new course announcement. Input: Announcement text body. Output: Announcement text body that was created."
    ),
    Tool(
        name="Upload Course material to cloud",
        func=upload_course_material_to_cloud,
        description="Upload course material to cloud storage. Input: blob_name. Output: URL of the uploaded file.",
    ),
    Tool(
        name="Evaluate MCQ tests and provide feedback",
        func= evaluate_mcq_test,
        description="Evaluate MCQ tests and provide feedback. Input: test_id. Output: url of the evaluation report",
    ),
    Tool(
        name= 'Get my Grades',
        func= get_grades,
        description="Get my grades for the tests I have taken. Input: None. Output: My grades for the tests I have taken no extra text or explanation is needed. Just return the grades in array.",
    ),
    Tool(
        name="Get student details with student_id",
        func = get_student_details,
        description="Get details of a student by their ID. Input: student_id. Output: Student details.",
    ),
]