# Fake Job & Internship Ad Detector

An AI-powered Streamlit application that analyzes job and internship advertisements for potential scam indicators.

## Project Overview

Fake job and internship advertisements can be used to deceive job seekers into paying money, sharing personal information, clicking suspicious links, or communicating with unverified employers.

This project uses Artificial Intelligence to analyze advertisement text and identify potential warning signs.

## Features

- AI-based job advertisement analysis
- Risk score from 0 to 100
- LOW, MEDIUM, and HIGH risk levels
- Potential red flag detection
- Positive signs
- Safety recommendations
- Simple Streamlit interface
- Groq API integration

## Technologies

- Python
- Streamlit
- Groq API
- Large Language Model (LLM)

## Workflow

1. User pastes a job or internship advertisement.
2. Streamlit receives the advertisement.
3. The application sends the text to the Groq API.
4. The AI analyzes potential scam indicators.
5. The AI generates a risk assessment.
6. Streamlit displays the risk level, score, red flags, and recommendations.

## Important Disclaimer

This application provides an indicative risk assessment based on the advertisement text.

It does not prove that an advertisement is definitely fake or genuine.

Users should independently verify the employer before sharing sensitive information, paying money, or accepting an offer.

## Project Structure

```text
Fake-Job-Detector/
│
├── app.py
├── requirements.txt
└── README.md
