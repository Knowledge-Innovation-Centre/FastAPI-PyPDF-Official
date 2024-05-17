# Timesheet PDF Generator and Email Sender

This FastAPI application allows users to generate PDF reports of timesheets and send them via email. The application is designed to process timesheet data, create a PDF report, and email it to the specified recipient.

# Features
## API Endpoints
- `GET /`: Root endpoint to verify that the application is running.
- `POST /send_data`: Endpoint to receive timesheet data, generate a PDF report, and send it via email.

## Timesheet PDF Generation
- Converts provided timesheet data into a structured PDF document.
- Includes tables for organization details, timesheet entries, total hours and wages, employee and employer signatures.

## Email Sending
- Uses SMTP to send the generated PDF report to the specified employer email.
- Email includes a subject and body with details about the report.

# Dependencies
- FastAPI
- Starlette
- smtplib
- email.mime
- fpdf
- environ
- unidecode

# Installation
## Clone the repository
- `git clone <repository_url>`
- `cd <repository_directory>`

## Install dependencies
- `pip3 install -r requirements.txt`

## Set up environment variables
- Create a `.env` file in the root directory.
- Define the following variables in the `.env` file
```bash
    SMTP_SERVER_0=<your_smtp_server>
    SMTP_LOGIN_EMAIL_0=<your_email>
    SMTP_PASSWORD_0=<your_email_password>
    MSG_FROM_0=<your_email>
```

## Usage
### Run the FastAPI application
`uvicorn main:app --host 0.0.0.0 --port 8080`

### Send a POST request to `/send_data` endpoint:
Example request body:
```json
{
  "user_name": "John Doe",
  "organisation": "ABC Corp",
  "date": "2024-05-17",
  "timesheets": [
    {
      "date": "2024-05-16",
      "wps": "Project X",
      "acts": ["Task A 5h", "Task B 3h"],
      "hours": 8,
      "wage": 200
    }
  ],
  "employer_email": "employer@example.com",
  "employer_name": "Jane Smith"
}
```