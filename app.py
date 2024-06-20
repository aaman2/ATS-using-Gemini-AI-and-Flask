from flask import Flask, render_template, request
import google.generativeai as genai
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()  # load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        jd = request.form['jd']
        uploaded_file = request.files['resume']

        if uploaded_file:
            text = input_pdf_text(uploaded_file)
            input_prompt = f"""
            Hey Act Like a skilled or very experience ATS(Application Tracking System)
            with a deep understanding of tech field, software engineering, data science, data analyst
            and big data engineer. Your task is to evaluate the resume based on the given job description.
            You must consider the job market is very competitive and you should provide 
            best assistance for improving thr resumes. Assign the percentage Matching based 
            on Jd and the missing keywords and Found keywords with high accuracy
            resume: {text}
            description: {jd}

            I want the response in one single string having the structure
            {{"JD Match":"%","MissingKeywords":[],"FoundKeywords":[],"Profile Summary":""}}
            """

            response = get_gemini_response(input_prompt)
            return render_template('result.html', response=response)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
