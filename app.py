
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime, timezone
from bson import ObjectId
import pymupdf as fitz
import certifi
import markdown
import bleach
import time
import re
from docx import Document
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()


# MongoDB Connection
mongo_uri = os.getenv("MONGO_URI")

mongo_client = MongoClient(mongo_uri)

db = mongo_client["ai_question_evaluation"]

users_collection = db["users"]
reports_collection = db["reports"]


# Gemini API Connection
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    client = genai.Client(
        api_key=GEMINI_API_KEY,
        http_options={"timeout": 120000}
    )
    print("Gemini API key loaded successfully!")
else:
    client = None
    print("Gemini API key not found!")


# Flask Configuration
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


# EMAIL VALIDATION
def is_valid_email(email):
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.fullmatch(pattern, email) is not None


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            return render_template(
                "login.html",
                error="Please enter your email and password!"
            )

        if not is_valid_email(email):
            return render_template(
                "login.html",
                error="Please enter a valid email address!"
            )

        user = users_collection.find_one({"email": email})

        if user and check_password_hash(user["password"], password):

            session["user_id"] = str(user["_id"])
            session["user_name"] = user["name"]

            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid email or password!"
        )

    return render_template("login.html")


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            return render_template(
                "register.html",
                error="Please fill in all fields!"
            )

        if not is_valid_email(email):
            return render_template(
                "register.html",
                error="Please enter a valid email address!"
            )

        existing_user = users_collection.find_one({"email": email})

        if existing_user:
            return render_template(
                "register.html",
                error="This email is already registered!"
            )

        hashed_password = generate_password_hash(password)

        user = {
            "name": name,
            "email": email,
            "password": hashed_password
        }

        users_collection.insert_one(user)

        return redirect(url_for("login"))

    return render_template("register.html")


# DASHBOARD
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")


# PREVIOUS REPORTS
@app.route("/history")
def history():

    if "user_id" not in session:
        return redirect(url_for("login"))

    reports = list(
        reports_collection.find(
            {"user_id": session["user_id"]}
        ).sort("created_at", -1)
    )

    return render_template(
        "history.html",
        reports=reports
    )


# VIEW INDIVIDUAL REPORT
@app.route("/report/<report_id>")
def view_report(report_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    try:

        report = reports_collection.find_one({
            "_id": ObjectId(report_id),
            "user_id": session["user_id"]
        })

        if not report:
            return "Report not found!", 404

        # Convert Markdown report into HTML
        report_html = markdown.markdown(
            report["evaluation_report"],
            extensions=["tables", "fenced_code"]
        )

        # Clean generated HTML for safety
        report_html = bleach.clean(
            report_html,
            tags=[
                "h1", "h2", "h3", "h4",
                "p", "br", "hr",
                "strong", "em",
                "ul", "ol", "li",
                "table", "thead", "tbody",
                "tr", "th", "td",
                "blockquote", "code", "pre"
            ],
            strip=True
        )

        return render_template(
            "view_report.html",
            report=report,
            report_html=report_html
        )

    except Exception as e:
        print("Report Error:", e)
        return "Invalid report ID!", 400


# LOGOUT
@app.route("/logout")
def logout():

    session.clear()

    response = redirect(url_for("login"))
    response.delete_cookie("session")

    return response


# EXTRACT TEXT FROM DOCUMENTS
def extract_text(file):

    filename = file.filename.lower()

    if filename.endswith(".pdf"):

        pdf = fitz.open(
            stream=file.read(),
            filetype="pdf"
        )

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


# GEMINI AI EVALUATION
def evaluate_with_gemini(course, targets, question_text, clo_text, plo_text=""):

    if client is None:
        raise Exception("Gemini API key is missing.")

    if plo_text.strip():

        plo_instructions = f"""
        PLO Document:
        {plo_text}

        3. Identify relevant PLOs and map questions to them where supported by the document.
        """

    else:

        plo_instructions = """
        PLO Document: Not provided.

        Do not perform PLO analysis.
        Do not invent or assume any PLOs.
        Clearly mention that PLO analysis was skipped because no PLO document was provided.
        """

    prompt = f"""
    You are an expert academic question paper evaluator.

    Course Name: {course}

    Target Distribution: {targets}

    Question Paper:
    {question_text}

    CLO Document:
    {clo_text}

    {plo_instructions}

    Evaluate the question paper.

    1. Classify each question as Theoretical, Analytical, or Mathematical.
    2. Match questions with the relevant CLOs.
    3. { "Identify relevant PLOs." if plo_text.strip() else "Skip PLO alignment because no PLO document was provided." }
    4. Calculate the actual question distribution.
    5. Compare actual distribution with the target distribution.
    6. Give recommendations.

    Prepare a clear evaluation report.

    Formatting instructions:

    - Write the entire report using valid Markdown syntax.
    - Start every main section with a Markdown heading using ##.
    - Use ### for subsections.
    - Put every bullet point on a separate line.
    - Put every numbered list item on a separate line.
    - Never combine multiple list items into one paragraph.
    - Use "- " for bullet points.
    - Never use escaped symbols such as "\\*".
    - Use proper numbered lists such as "1. ", "2. ", "3. ".
    - Use Markdown tables for question classifications and distribution comparisons.
    - Put a blank line before and after every heading, list, and table.
    - Keep paragraphs short and readable.
    - Do not use unnecessary indentation.
    - Do not write list items as inline text separated by asterisks.
    - Do not invent information that is missing from the documents.
    - Make sure section numbers are visible and consistent.

    Example of correct formatting:

    ## 4. Actual Question Distribution

    Assuming equal weightage per question:

    - Total Questions: 6
    - Theoretical: 3 questions (Q1, Q2, Q6) = 50%
    - Analytical: 1 question (Q5) = 16.67%
    - Mathematical: 2 questions (Q3, Q4) = 33.33%

    ## 5. Recommendations

    1. Review the theoretical question distribution.
    2. Improve the analytical question coverage.
    3. Maintain the mathematical question balance.
    """

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            if not response.text:
                raise Exception("Gemini returned an empty response.")

            return response.text

        except Exception as e:

            error_message = str(e)

            if "503" in error_message and attempt < 2:

                wait_time = 5 * (2 ** attempt)

                print(
                    f"Gemini server busy. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:
                raise


# HOME PAGE
@app.route("/")
def home():
    return redirect(url_for("login"))


# EVALUATION PAGE
@app.route("/evaluate-page")
def evaluate_page():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("index.html")


# EVALUATE QUESTION PAPER
@app.route("/evaluate", methods=["POST"])
def evaluate():

    # Login protection
    if "user_id" not in session:
        return jsonify({
            "error": "Please log in before evaluating a question paper."
        }), 401

    course = request.form.get("course")
    targets = request.form.get("targets")

    question_file = request.files.get("question_paper")
    clo_file = request.files.get("clo_file")
    plo_file = request.files.get("plo_file")

    # Check required text fields
    if not course or not targets:
        return jsonify({
            "error": "Please enter course name and target distribution."
        }), 400

    # Check required documents
    if (
        not question_file
        or not question_file.filename
        or not clo_file
        or not clo_file.filename
    ):
        return jsonify({
            "error": "Please upload the Question Paper and CLO Document."
        }), 400

    allowed_extensions = {"pdf", "docx", "txt"}

    # Validate required documents
    for file in [question_file, clo_file]:

        extension = file.filename.rsplit(".", 1)[-1].lower()

        if extension not in allowed_extensions:
            return jsonify({
                "error": "Only PDF, DOCX and TXT files are allowed."
            }), 400

    # Validate optional PLO document only when uploaded
    if plo_file and plo_file.filename:

        extension = plo_file.filename.rsplit(".", 1)[-1].lower()

        if extension not in allowed_extensions:
            return jsonify({
                "error": "PLO document must be PDF, DOCX or TXT."
            }), 400

    print("Course:", course)
    print("Target Distribution:", targets)

    try:

        # Extract required documents
        question_text = extract_text(question_file)
        clo_text = extract_text(clo_file)

        # Extract optional PLO document
        plo_text = ""

        if plo_file and plo_file.filename:
            plo_text = extract_text(plo_file)

        print("Documents extracted successfully!")
        print("Question paper characters:", len(question_text))
        print("CLO characters:", len(clo_text))
        print("PLO characters:", len(plo_text))

        evaluation_report = evaluate_with_gemini(
            course,
            targets,
            question_text,
            clo_text,
            plo_text
        )

        # Save report in MongoDB
        report = {
            "user_id": session["user_id"],
            "course": course,
            "targets": targets,
            "evaluation_report": evaluation_report,
            "created_at": datetime.now(timezone.utc)
        }

        reports_collection.insert_one(report)

        print("Evaluation report saved successfully!")

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


# RUN APPLICATION
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
