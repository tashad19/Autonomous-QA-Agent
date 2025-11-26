# Autonomous QA Agent for Test Case and Selenium Script Generation

## Overview
This project builds an autonomous QA assistant that ingests support documents and a checkout.html page, creates a knowledge base, and generates documentation-grounded test cases and Python Selenium scripts.

The system uses FastAPI for backend processing, Streamlit for the UI, a vector database for retrieval, and lightweight embeddings to ground reasoning in uploaded files.

## Features
• Upload support documents  
• Upload checkout.html  
• Build knowledge base  
• Generate test cases using RAG  
• Select a test case and generate Selenium scripts  
• Scripts use selectors from actual HTML structure  

## Folder Structure
```
autonomous-qa-agent/
├─ app/
│ ├─ main.py
│ ├─ routes/
│ ├─ models/
│ └─ core/
├─ scripts/
├─ assets/
├─ ui.py
├─ README.md
└─ requirements.txt
```

## Setup

### 1. Create a virtual environment
```
python -m venv venv
source venv/bin/activate (Mac/Linux)
venv\Scripts\activate (Windows)
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

## Running the backend
```
python -m app.main
```

## Running the Streamlit UI
```
streamlit run ui.py
```

## Usage Flow
1. Open the Streamlit UI.  
2. Upload support documents.  
3. Upload the checkout.html page.  
4. Build knowledge base.  
5. Enter a query such as:  
   Generate test cases for the discount code feature.
6. Pick a test case and generate Selenium scripts.

## Notes
• The LLM logic is modular and can be replaced with any model.  
• The Selenium generator uses heuristic selector extraction.  
• All reasoning is grounded strictly in uploaded documents.  
