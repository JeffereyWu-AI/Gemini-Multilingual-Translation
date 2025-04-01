# LLM-Powered Multilingual Translation Service

## Project Overview
This is a real-time translation service built with FastAPI, supporting multi-language translation and storing translation results in a database. Users can submit translation requests through a frontend interface and view the translation results.

## Features
- **Multi-Language Translation**: Supports translating text into multiple languages.
- **Background Task Processing**: Uses FastAPI's `BackgroundTasks` to handle translation tasks asynchronously.
- **Database Storage**: Uses SQLAlchemy to store translation requests and results in a database.
- **Frontend Interface**: Provides a simple frontend page where users can submit translation requests via a form.

## Tech Stack
- **Backend Framework**: FastAPI
- **Database**: SQLAlchemy
- **Frontend**: HTML, JavaScript, Bootstrap
- **Translation Service**: Google LLM Gemini API


### Start the Server
```bash
uvicorn app.main:app --reload
```

## Usage

### 1. Access the Frontend Page
Open your browser and navigate to `http://localhost:8000/index` to view the translation service homepage.

### 2. Submit a Translation Request
Enter the text to be translated and the target languages (separated by commas) in the form, then click the "Translate" button to submit the request.

### 3. View Translation Results
After submitting the request, the page will redirect to the results page, displaying the status and results of the translation.

## Project Structure
```
real-time-translation/
├── app/
│   ├── main.py                # FastAPI main application
│   ├── database.py            # Database configuration
│   ├── models.py              # Database models
│   ├── schemas.py             # Pydantic models
│   ├── utils.py               # Translation utility functions
│   └── templates/             # Frontend template files
│       ├── index.html         # Homepage
│       └── results.html       # Translation results page
├── .env                       # Environment variables file
├── requirements.txt           # Dependencies file
└── README.md                  # Project documentation
```




### Additional Notes
- Replace `your-username` with your GitHub username.
- If you use a different translation service (e.g., Google Translate API), update the `API_KEY` description.
- If the project has additional dependencies or configurations, add them to the **Installation Steps** section.

This README should help you effectively showcase your project!
