from pathlib import Path
from kerykeion import AstrologicalSubject, KerykeionChartSVG
from io import BytesIO
from starlette.responses import StreamingResponse, FileResponse, Response
import cairosvg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText
import os


app = FastAPI()


class EmailSchema(BaseModel):
    recipient: EmailStr
    subject: str
    message: str


class UserInfo(BaseModel):
    name: str
    birth_time: str
    birth_date: str
    birth_city: str
    email: EmailStr


@app.post("/send-email/")
def send_email(user_info: UserInfo, email: EmailSchema):
    sender_email = os.environ.get('SENDER_EMAIL')
    app_password = os.environ.get('SENDER_PASSWORD')

    msg = MIMEText(f"Name: {user_info.name}\nBirth Time: {user_info.birth_time}\nBirth Date: {user_info.birth_date}\nBirth City: {user_info.birth_city}\n\n{email.message}")
    msg['Subject'] = email.subject
    msg['From'] = sender_email
    msg['To'] = email.recipient

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)

        server.sendmail(sender_email, email.recipient, msg.as_string())
        server.quit()
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")


@app.get("/make_svg")
def make_svg(name: str, year: int, month: int, day: int, hour: int, minute: int, city: str):
    kanye = AstrologicalSubject(name, year, month, day, hour, minute, city)
    name = KerykeionChartSVG(kanye, chart_type="Natal")

    image_data = cairosvg.svg2png(name.template)
    image_stream = BytesIO(image_data)

    return StreamingResponse(image_stream)


@app.get("/make_full_svg")
def make_svg(name: str, year: int, month: int, day: int, hour: int, minute: int, city: str):
    kanye = AstrologicalSubject(name, year, month, day, hour, minute, city)

    pic = KerykeionChartSVG(kanye, chart_type="Natal")
    pic.set_output_directory(Path('./charts'))
    pic.makeSVG()

    return FileResponse(f'{str(pic.chartname)}')


@app.get("/get_svg_code")
def make_svg(name: str, year: int, month: int, day: int, hour: int, minute: int, city: str):
    kanye = AstrologicalSubject(name, year, month, day, hour, minute, city)

    pic = KerykeionChartSVG(kanye, chart_type="Natal")

    return Response(content=pic.template, media_type="image/svg+xml")


@app.get("/download_full_svg")
def make_svg(name: str, year: int, month: int, day: int, hour: int, minute: int, city: str):
    kanye = AstrologicalSubject(name, year, month, day, hour, minute, city)

    pic = KerykeionChartSVG(kanye, chart_type="Natal")
    pic.set_output_directory(Path('./charts'))
    pic.makeSVG()

    return FileResponse(f'{str(pic.chartname)}', filename='natalchart.svg', media_type='application/octet-stream')
