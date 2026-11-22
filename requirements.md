# AI-Based Question Set Evaluation System

## 1. Project Overview

This project aims to develop an AI-based web application that helps teachers evaluate examination question papers based on Course Learning Outcomes (CLOs), Program Learning Outcomes (PLOs), and question types.

The system uses AI to analyze uploaded question papers, classify questions, evaluate CLO and PLO alignment, compare actual question distribution with the teacher's target distribution, and generate evaluation reports.

## 2. Project Objectives

1. To develop a user-friendly web application for teachers.
2. To provide secure user registration and login.
3. To collect course information and learning outcomes.
4. To classify questions as mathematical, analytical, or theoretical using AI.
5. To evaluate question alignment with CLOs.
6. To identify relevant PLOs for examination questions.
7. To compare actual question distribution with the teacher's target distribution.
8. To generate evaluation reports with recommendations.
9. To save evaluation reports and allow teachers to view previous reports.

## 3. Functional Requirements

### 3.1 User Authentication

1. Users can register for a new account.
2. Registered users can log in securely.
3. Users can log out of their accounts.
4. The system will maintain user sessions.
5. Only authenticated users can access the dashboard and evaluation features.

### 3.2 Dashboard and Evaluation

1. Teachers can access a dashboard after logging in.
2. Teachers can enter course names.
3. Teachers can provide CLOs and PLOs.
4. Teachers can specify target question distribution.
5. Teachers can upload examination question papers in PDF, DOCX, or TXT format.
6. Teachers can upload CLO and PLO documents.
7. The system will validate required inputs.
8. The system will extract text from uploaded documents.
9. The system will analyze questions using the Google Gemini API.
10. The system will classify questions as mathematical, analytical, or theoretical.
11. The system will evaluate question alignment with CLOs and identify relevant PLOs.
12. The system will calculate actual question distribution.
13. The system will compare actual distribution with the teacher's target distribution.
14. The system will generate evaluation reports with recommendations.

### 3.3 Report Management

1. The system will save evaluation reports in MongoDB.
2. Teachers can view their previous evaluation reports.
3. Each teacher can access their own saved reports.

## 4. Non-Functional Requirements

1. The website should be easy to use.
2. The interface should have a professional and modern design.
3. The website should be responsive on desktop, tablet, and mobile devices.
4. The system should provide clear and readable evaluation results.
5. The system should handle invalid inputs and errors properly.
6. The system should protect user information and submitted documents.
7. The system should provide secure user authentication and session management.

## 5. Technologies

**Frontend:** HTML, CSS, JavaScript

**Backend:** Python, Flask

**AI:** Google Gemini API

**Database:** MongoDB

**Document Processing:** PyMuPDF, python-docx

**Development Tool:** Visual Studio Code

**Version Control:** Git and GitHub

## 6. Development Plan

**Day 1:** Frontend design, input validation, wireframe, and use case diagram.

**Day 2:** Python Flask backend and frontend-backend communication.

**Day 3:** Gemini API integration, document upload and text extraction, AI-based question evaluation, MongoDB integration, user authentication, dashboard, report management, responsive UI/UX, testing, and final documentation.
