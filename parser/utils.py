import google.generativeai as genai
from django.core.files.uploadedfile import UploadedFile
import fitz, os, json
from dotenv import load_dotenv
from django.core.exceptions import ValidationError
import re

load_dotenv()

# Configure Google GenAI with API key
genai.configure(api_key=os.getenv("API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

# Function to extract text from uploaded PDF
def read_uploaded_file(file_object: UploadedFile, file_extension: str) -> str:
    file_content = file_object.read()
    
    # Use fitz to read the PDF content
    with fitz.open(stream=file_content, filetype=file_extension) as document:
        text = ''
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text += page.get_text()
        return text

# Prompt for resume extraction
prompt_data = """
    You are an AI professional resume scoring system. You will receive the content of a resume and evaluate it based on industry standards for format, clarity, relevant experience, and skills. Before start scoring, forget the previous resume you have seen.
Provide the following:
1. A score between 1 and 100 for the overall quality of the resume based upon the content and the depth of the content like skills, experience, education, etc. Keep the score dynamic based on the content of the resume. Show section wise score and the overall score. Consider the hard competition for the role and the candidate's potential for scoring the role.
2. A list of suggested improvements for the resume, including format, content, and any missing sections or skills that would improve the candidate's chances.
3. Used fixed keys in the JSON response: 'overall_score', 'section_scores', and 'improvements'.
Return the response in the JSON format only.
"""

# Function to extract resume info using Google GenAI
def extract_resume_info(file_content: str):
    try:
        # Create the request body with the prompt and resume content
        prompt = prompt_data + "Resume Content: " + file_content

        # Call the Google GenAI model and pass the content
        response = model.generate_content(prompt)
        
        # Extract the text from the response
        response_text = response.text.strip()
        
        # Check if the response is wrapped in a code block
        code_block_pattern = r'```(?:json)?\n(.*)\n```'
        match = re.search(code_block_pattern, response_text, re.DOTALL)
        if match:
            response_text = match.group(1).strip()
        
        # Check if the response starts and ends with curly braces
        if not (response_text.startswith('{') and response_text.endswith('}')):
            raise ValueError("Response is not in the expected JSON format")
        
        # Parse the JSON string
        parsed_response = json.loads(response_text)
        return parsed_response
    
    except json.JSONDecodeError as e:
        raise ValidationError(f"Failed to parse JSON response: {e}. Response: {response_text}")
    except ValueError as e:
        raise ValidationError(f"Invalid response format: {e}. Response: {response_text}")
    except Exception as e:
        raise ValidationError(f"Something went wrong: {e}")