# AI-Based Question Set Evaluation System

An AI-powered web application that helps teachers evaluate examination question papers based on Course Learning Outcomes (CLOs), Program Learning Outcomes (PLOs), and question types.

## Project Overview

The system uses Google Gemini AI to analyze examination question papers, classify questions, evaluate CLO and PLO alignment, compare actual question distribution with target distribution, and generate evaluation reports with recommendations.

## Key Features

- User registration and login
- Secure authentication and session management
- Teacher dashboard
- Course information and learning outcome input
- Question paper upload (PDF, DOCX, and TXT)
- Automatic document text extraction
- AI-based question classification:
  - Theoretical
  - Analytical
  - Mathematical
- CLO alignment evaluation
- PLO mapping
- Target vs. actual question distribution comparison
- AI-generated evaluation reports and recommendations
- MongoDB-based report storage
- Previous evaluation report history
- Responsive and user-friendly interface

## Technologies Used

| Component           | Technology            |
| ------------------- | --------------------- |
| Frontend            | HTML, CSS, JavaScript |
| Backend             | Python, Flask         |
| AI Integration      | Google Gemini API     |
| Database            | MongoDB               |
| Document Processing | PyMuPDF, python-docx  |
| Code Editor         | Visual Studio Code    |
| Version Control     | Git and GitHub        |

## Project Structure

```text
AI-Question-Evaluation-System/
├── static/
│   ├── style.css
│   └── script.js
├── templates/
│   └── index.html
├── app.py
├── test_gemini.py
├── requirements.md
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Sazzad-012/AI-Question-Evaluation-System.git
```

### 2. Open the Project Folder

```bash
cd AI-Question-Evaluation-System
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

For Windows Git Bash:

```bash
source .venv/Scripts/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure the Gemini API Key

Create a `.env` file in the project root directory:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace `your_gemini_api_key` with your own API key.

**Important:** Never upload your `.env` file or expose your API key on GitHub.

### 7. Run the Application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

## Development Plan

- **Day 1:** Frontend design, input validation, wireframe, and use case diagram.
- **Day 2:** Python Flask backend and frontend-backend communication.
- **Day 3:** Gemini API integration, document processing, AI evaluation, MongoDB integration, authentication, dashboard, report management, responsive UI/UX, testing, and documentation.

## Project Repository

GitHub: https://github.com/Sazzad-012/AI-Question-Evaluation-System
