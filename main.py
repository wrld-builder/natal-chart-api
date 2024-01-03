from fastapi import FastAPI
from kerykeion import AstrologicalSubject, KerykeionChartSVG
from io import BytesIO
from starlette.responses import StreamingResponse, JSONResponse
import cairosvg
import json


class DataHelper:
    @staticmethod
    def zodiac_sign(day, month):
        if (month == 3 and day >= 21) or (month == 4 and day <= 19):
            return "Овен"
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return "Телец"
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            return "Близнецы"
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            return "Рак"
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            return "Лев"
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            return "Дева"
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            return "Весы"
        elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
            return "Скорпион"
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            return "Стрелец"
        elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
            return "Козерог"
        elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
            return "Водолей"
        else:
            return "Рыбы"


app = FastAPI()


@app.get("/make_svg")
def make_svg(name: str, year: int, month: int, day: int, hour: int, minute: int, city: str):
    kanye = AstrologicalSubject(name, year, month, day, hour, minute, city)
    name = KerykeionChartSVG(kanye, chart_type="Natal")

    image_data = cairosvg.svg2png(name.template)
    image_stream = BytesIO(image_data)

    return StreamingResponse(image_stream)


@app.get('/calculate')
def calculate(name: str, year: int, month: int, day: int, hour: int, minute: int, city: str):
    kanye = AstrologicalSubject(name, year, month, day, hour, minute, city)

    kanye_data = json.loads(kanye.json(dump=False))
    kanye_data['zodiac_sign'] = DataHelper.zodiac_sign(day, month)

    return JSONResponse(kanye_data)
