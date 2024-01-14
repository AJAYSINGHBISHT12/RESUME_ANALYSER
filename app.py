import openai
import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from datetime import datetime

def extract_text_by_page(pdf_path, additional_texts=[]):
    extracted_text = ""
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            converter = TextConverter(resource_manager, fake_file_handle)
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)
            text = fake_file_handle.getvalue()
            extracted_text += text
            # close open handles
            converter.close()
            fake_file_handle.close()

    # Add additional texts to the extracted content
    extracted_text += " ".join(additional_texts)

    return extracted_text

def openai_analysis(text):
    # Use OpenAI API to analyze the text and get responses
    openai.api_key = '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'
    responses = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",  # Use the latest supported model
        prompt=text,
        max_tokens=150
    )

    return responses.choices[0].text.strip()

def analyze_resume(resume_text, today_date):
    # Pass the entire resume text for OpenAI analysis
    openai_output = openai_analysis(resume_text)

    # Print the OpenAI analysis output
    print("OpenAI Analysis Output:")
    print(openai_output)
    print('=' * 50)

if __name__ == '__main__':
    pdf_path = 'AjayResume.pdf'
    today_date = datetime.now().strftime("%d/%m/%Y")
    additional_texts = [" This is the extracted text from the Resume. From this I want only specific information in a systematic way based on these points:",
                        "1- Name and Contact number",
                        "2-Skills",
                        "3-Graduation year",
                        "4-in the resume text, find the graduation year of the candidate. Calculate the gap duration from the graduation year to the present as the gap year. Exclude specific intervals mentioned in the resume, like work experience or other educational programs, from this gap calculation. Check if there is a gap between the graduation year and the current date after excluding these specified intervals. If there is a gap, extract and print the duration of the gap in years and months,and from when to when. today's date is {}. Thank you!".format(today_date, "{}")
,
                        "5-dummy project: if the person's projects include any of the following: Tic-Tac-Toe , Blog, Personal Portfolio Website, Library Management System, To-Do List Application, or Weather App. Print the information that dummy projects are present; otherwise, no dummy projects",
                        "6- In this, we have to list the projects of that person from the following fields and list the number of projects in each field: Software development, AI and ML, or Web development."
    ]

    resume_text = extract_text_by_page(pdf_path, additional_texts)
    analyze_resume(resume_text, today_date)
