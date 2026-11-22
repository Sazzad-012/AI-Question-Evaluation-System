from flask import Flask, request, jsonify, render_template
import pymupdf as fitz
import time
from docx import Document
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
    print("Gemini API key loaded successfully!")
else:
    client = None
    print("Gemini API key not found!")

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


def extract_text(file):

    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        pdf = fitz.open(stream=file.read(), filetype="pdf")

        text = ""

        for page in pdf:
            text += page.get_text()

        return text

    elif filename.endswith(".docx"):
        document = Document(file)

        text = ""

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

        return text

    elif filename.endswith(".txt"):
        return file.read().decode("utf-8")

    return ""



def evaluate_with_gemini(course, targets, question_text, clo_text, plo_text):

    if client is None:
        raise Exception("Gemini API key is missing.")

    prompt = f"""
    You are an expert academic question paper evaluator.

    Course Name: {course}

    Target Distribution: {targets}

    Question Paper:
    {question_text}

    CLO Document:
    {clo_text}

    PLO Document:
    {plo_text}

    Evaluate the question paper.

    1. Classify each question as Theoretical, Analytical, or Mathematical.
    2. Match questions with the relevant CLOs.
    3. Identify relevant PLOs.
    4. Calculate the actual question distribution.
    5. Compare actual distribution with the target distribution.
    6. Give recommendations.

    Prepare a clear evaluation report.
    Do not invent information that is missing from the documents.
    """

    for attempt in range(2):

        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            if "503" in str(e) and attempt < 1:
                print("Gemini server busy. Retrying...")
                time.sleep(2)

            else:
                raise


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/evaluate", methods=["POST"])
def evaluate():

    course = request.form.get("course")
    targets = request.form.get("targets")

    question_file = request.files.get("question_paper")
    clo_file = request.files.get("clo_file")
    plo_file = request.files.get("plo_file")

    if not course or not targets:
        return jsonify({
            "error": "Please enter course name and target distribution."
        }), 400

    if not question_file or not clo_file or not plo_file:
        return jsonify({
            "error": "Please upload all three documents."
        }), 400

    allowed_extensions = {"pdf", "docx", "txt"}

    for file in [question_file, clo_file, plo_file]:

        extension = file.filename.rsplit(".", 1)[-1].lower()

        if extension not in allowed_extensions:
            return jsonify({
                "error": "Only PDF, DOCX and TXT files are allowed."
            }), 400

    print("Course:", course)
    print("Target Distribution:", targets)

    question_text = extract_text(question_file)
    clo_text = extract_text(clo_file)
    plo_text = extract_text(plo_file)

    print("Documents extracted successfully!")

    try:

        evaluation_report = evaluate_with_gemini(
            course,
            targets,
            question_text,
            clo_text,
            plo_text
        )

        return jsonify({
            "message": "AI evaluation completed successfully!",
            "evaluation_report": evaluation_report
        })

    except Exception as e:

        error_message = str(e)

        print("Gemini Error:", error_message)

        if "429" in error_message:
            return jsonify({
                "error": "Gemini request limit reached. Please wait before trying again."
            }), 429

        elif "503" in error_message:
            return jsonify({
                "error": "Gemini server is currently busy. Please try again later."
            }), 503

        else:
            return jsonify({
                "error": "AI evaluation failed. Please check the server or API configuration."
            }), 500


if __name__ == "__main__":
    app.run(debug=True)
