from fastapi import FastAPI, Path, Query, Request, BackgroundTasks
from typing import Optional
from pydantic import BaseModel

from starlette.responses import JSONResponse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from table_function import PDF
from fastapi.responses import FileResponse
from io import BytesIO


data = [
    ["First name", "Last name", "Age", "City",], # 'testing','size'],
    ["Jules", "Smith", "34", "San Juan",], # 'testing','size'],
    ["Mary", "Ramos", "45", "Orlando",], # 'testing','size'],
    ["Carlson", "Banks", "19", "Los Angeles",], # 'testing','size'],
    ["Lucas", "Cimon", "31", "Saint-Mahturin-sur-Loire",], # 'testing','size'],
]

data_as_dict = {"First name": ["Jules","Mary","Carlson","Lucas"],
                "Last name": ["Smith","Ramos","Banks","Cimon"],
                "Age": [34,'45','19','31']
            }



app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Congratz! You've made it!!!"}


@app.post("/send_data")
async def create_pdf(request: Request):
    
    obj = await request.json()

    # Create the message
    msg = MIMEMultipart()
    msg["From"] = "2020822438@student.uitm.edu.my"
    msg["To"] = obj["user_email"]
    msg["Subject"] = "Timesheets"


    # Add message body
    body = "This is the message body"
    msg.attach(MIMEText(body))


    # Attach the file
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Times", size=10)

    pdf.create_table(table_data = data,title='I\'m the first title', cell_width='even')
    pdf.ln()

    in_memory_file = BytesIO(pdf.output())
    attach = MIMEApplication(in_memory_file.read(), _subtype="pdf")
    attach.add_header("Content-Disposition", "attachment", filename=str("PDF_FILE.pdf"))
    msg.attach(attach)


    # Send the message
    smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_server.starttls()
    smtp_server.login("2020822438@student.uitm.edu.my", "emcwvngjzaiurfrx")
    smtp_server.sendmail("2020822438@student.uitm.edu.my", obj["user_email"], msg.as_string())
    smtp_server.quit()

    return {"message": f"Email Sent to {obj['user_email']}"}


    # return {"user_email": obj["user_email"],
    #         "organisation": obj["organisation"]}


@app.post("/predict")
async def predict(request: Request):

    obj = await request.json()
    return {"message": "Data Received",
            "data": obj["data"]}


