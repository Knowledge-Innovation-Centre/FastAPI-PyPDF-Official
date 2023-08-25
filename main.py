from fastapi import FastAPI, Path, Query, Request, BackgroundTasks
from typing import Optional
from pydantic import BaseModel

from starlette.responses import JSONResponse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from fastapi.responses import FileResponse
from io import BytesIO

import warnings
warnings.filterwarnings("ignore")

from custom_class import PDF
from fpdf.fonts import FontFace

import environ


app = FastAPI()

env = environ.Env()
environ.Env.read_env()

@app.get("/")
async def root():
    return {"message": "Congratz! You've made it!!!"}


@app.post("/send_data")
async def create_pdf(request: Request):
    
    try:
        data = await request.json()


        # First Table
        user_name_unicode = str(data["name"], "utf-8")
        first_table = (
            ("Organization:", data["organisation"]),
            ("Name & Surname of Employee:", user_name_unicode),
            ("Date & Time of Report:", data["date"])
        )

        # Second Table
        second_table = [
            ("Date", "Work Packages", "Activities", "Hours", "Daily Wage (EUR)"),
        ]

        total_hours = 0
        total_wage = 0

        for timesheet in data["timesheets"]:
            ts_0 = timesheet[0]

            acts = ts_0["acts"]
            temp_list = []

            for act in acts:
                split = act.split(" ")
                # temp_list.append(f"{split[0]} {split[1]}")
                temp_list.append(f"{split[1]}")

            activities = ", ".join(temp_list)

            temp = tuple([ts_0["date"], ts_0["wps"], activities, str(ts_0["hours"]), str(ts_0["wage"])])

            total_hours = total_hours + ts_0["hours"]
            total_wage = total_wage + ts_0["wage"]
            
            second_table.append(temp)


        # Third Table
        third_table = (
            ("Total Hours", str(round(total_hours, 2))),
            ("Total Wage (EUR)", str(round(total_wage, 2)))
        )


        # Fourth Table
        fourth_table = (
            ("Name of the Employee", data["user_name"]),
            ("Date", ""),
            ("Signature of Employee", "")
        )


        # Fifth Table
        fifth_table = (
            ("Name of the Employer", ""),
            ("Date", ""),
            ("Signature of Employer", "")
        )


        #########################
        # Create the message
        msg = MIMEMultipart()
        msg["From"] = env("MSG_FROM_0")
        msg["To"] = data["employer_email"]
        msg["Subject"] = f"Requested Timesheets Report by {data['employer_name']} on {data['date']}"


        #########################
        # Add message body
        body = f"Dear {data['employer_name']},\n\nThis is a generated email. Per request, please see attached Timesheet Report in the PDF format for the signing process.\n\nIn case of any problems check the administrator in your organisation."


        # body = """Dear Receiver,

        #           This is a generated email. Per request, please see attached Timesheet Report in the PDF format for the signing process.

        #           In case of any problems check the administrator in your organisation."""
        msg.attach(MIMEText(body))


        #########################
        # Attach the file
        pdf = PDF()
        pdf.alias_nb_pages()
        pdf.set_auto_page_break(auto=True, margin=15)

        pdf.add_page()


        with pdf.table(text_align=("LEFT", "CENTER"), cell_fill_mode="ROWS", first_row_as_headings=False) as table:
            for data_row in first_table:
                row = table.row()
                index = 0
                for datum in data_row:
                    pdf.set_font("times", "", 12)
                    if index == 0:
                        pdf.set_font("times", "B", 12)
                        index += 1

                    row.cell(datum)


        pdf.ln(10)
        pdf.set_font("times", "", 12)
        grey = (216, 216, 216)
        second_table = tuple(second_table)

        style = FontFace(emphasis="BOLD", fill_color=grey)

        with pdf.table(text_align=("CENTER"), cell_fill_mode="ROWS", headings_style=style) as table:
            for data_row in second_table:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)


        if pdf.will_page_break(15):
            pdf.add_page()
        
        
        pdf.set_font("times", "", 12)
        with pdf.table(text_align=("CENTER", "CENTER"), cell_fill_mode="NONE", first_row_as_headings=False, cell_fill_color=grey) as table:
            for data_row in third_table:
                row = table.row()
                index = 0
                for datum in data_row:
                    pdf.set_font("times", "", 12)
                    pdf.set_fill_color(255,255,255)
                    if index == 0:
                        pdf.set_font("times", "B", 12)
                        pdf.set_fill_color(grey)
                        index += 1

                    row.cell(datum)


        if pdf.will_page_break(57):
            pdf.add_page()
        else:
            pdf.ln(10)
        

        pdf.set_font("times", "", 12)
        # pdf.add_page()
        # pdf.ln(10)
        with pdf.table(text_align=("LEFT", "CENTER"), cell_fill_mode="ROWS", first_row_as_headings=False, line_height=3 * pdf.font_size) as table:
            for data_row in fourth_table:
                row = table.row()
                index = 0
                for datum in data_row:
                    pdf.set_font("times", "", 14)
                    if index == 0:
                        pdf.set_font("times", "B", 12)
                        index += 1

                    row.cell(datum)


        if pdf.will_page_break(57):
            pdf.add_page()
        else:
            pdf.ln(10)
            

        pdf.set_font("times", "", 12)
        # pdf.add_page()
        # pdf.ln(10)
        with pdf.table(text_align=("LEFT", "CENTER"), cell_fill_mode="ROWS", first_row_as_headings=False, line_height=3 * pdf.font_size) as table:
            for data_row in fifth_table:
                row = table.row()
                index = 0
                for datum in data_row:
                    pdf.set_font("times", "", 14)
                    if index == 0:
                        pdf.set_font("times", "B", 12)
                        index += 1

                    row.cell(datum)


        #########################
        in_memory_file = BytesIO(pdf.output())
        attach = MIMEApplication(in_memory_file.read(), _subtype="pdf")
        custom_filename = f"Timesheets_Report_{data['user_name']}_{data['date']}"
        attach.add_header("Content-Disposition", "attachment", filename=str(custom_filename))
        msg.attach(attach)


        #########################
        # Send the message
        smtp_server = smtplib.SMTP(env("SMTP_SERVER_0"), 587)
        smtp_server.starttls()
        

        smtp_server.login(env("SMTP_LOGIN_EMAIL_0"), env("SMTP_PASSWORD_0"))
        smtp_server.sendmail(env("SMTP_LOGIN_EMAIL_0"), data["employer_email"], msg.as_string())


        smtp_server.quit()


        return {"status": 200}
        # return {"message": f"Email Sent to {data['employer_email']}"}
    except Exception:
        return {"status": 500}
        # return {"message": f"Email Sent to {data['user_email']}"}



