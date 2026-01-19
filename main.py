from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ----- Serve HTML -----
@app.get("/")
def read_index():
    return FileResponse(os.path.join(BASE_DIR, "static", "index.html"))

# ----- Quiz API -----
class QuizRequest(BaseModel):
    topic: str
    num_questions: int

class Question(BaseModel):
    question: str
    options: list[str]
    answer: str

class QuizResponse(BaseModel):
    topic: str
    quiz: list[Question]

QUESTION_BANK = {
    "math": [
        {"question":"5 + 3 = ?","options":["6","7","8","9"],"answer":"8"},
        {"question":"7 × 6 = ?","options":["36","40","42","48"],"answer":"42"},
        {"question":"10 ÷ 2 = ?","options":["2","4","5","10"],"answer":"5"},
        {"question":"Square of 9?","options":["18","27","72","81"],"answer":"81"},
        {"question":"Square root of 25?","options":["3","4","5","6"],"answer":"5"},
        {"question":"15 − 7 = ?","options":["6","7","8","9"],"answer":"8"},
        {"question":"12 × 4 = ?","options":["36","40","48","52"],"answer":"48"},
        {"question":"20 ÷ 5 = ?","options":["2","4","5","10"],"answer":"4"},
        {"question":"Cube of 3?","options":["6","9","18","27"],"answer":"27"},
        {"question":"100 − 45 = ?","options":["45","50","55","60"],"answer":"55"}
    ],

    "science": [
        {"question":"Gas we breathe?","options":["CO2","O2","N2","H2"],"answer":"O2"},
        {"question":"Sun is a?","options":["Planet","Star","Moon","Asteroid"],"answer":"Star"},
        {"question":"Water formula?","options":["H2O","CO2","O2","NaCl"],"answer":"H2O"},
        {"question":"Chemical symbol for gold?","options":["Au","Ag","Go","Gd"],"answer":"Au"},
        {"question":"Largest planet?","options":["Earth","Mars","Jupiter","Venus"],"answer":"Jupiter"},
        {"question":"Human heart chambers?","options":["2","3","4","5"],"answer":"4"},
        {"question":"Vitamin from sun?","options":["A","B","C","D"],"answer":"D"},
        {"question":"Boiling point of water?","options":["50°C","100°C","150°C","200°C"],"answer":"100°C"},
        {"question":"Gas plants release?","options":["O2","CO2","N2","H2"],"answer":"O2"},
        {"question":"Our galaxy name?","options":["Milky Way","Andromeda","Orion","Nova"],"answer":"Milky Way"}
    ],

    "history": [
        {"question":"Who discovered America?","options":["Columbus","Vasco","Magellan","Cook"],"answer":"Columbus"},
        {"question":"French Revolution year?","options":["1789","1776","1804","1812"],"answer":"1789"},
        {"question":"First President of India?","options":["Nehru","Rajendra Prasad","Gandhi","Patel"],"answer":"Rajendra Prasad"},
        {"question":"Who built Taj Mahal?","options":["Akbar","Shah Jahan","Babur","Aurangzeb"],"answer":"Shah Jahan"},
        {"question":"World War II ended?","options":["1942","1945","1950","1939"],"answer":"1945"},
        {"question":"Father of Nation (India)?","options":["Nehru","Gandhi","Patel","Bose"],"answer":"Gandhi"},
        {"question":"Mughal founder?","options":["Akbar","Babur","Humayun","Aurangzeb"],"answer":"Babur"},
        {"question":"Quit India year?","options":["1930","1942","1947","1950"],"answer":"1942"},
        {"question":"First man on moon?","options":["Armstrong","Aldrin","Yuri","Gagarin"],"answer":"Armstrong"},
        {"question":"Roman Empire fell?","options":["300","476","500","600"],"answer":"476"}
    ],

    "geography": [
        {"question":"Largest ocean?","options":["Indian","Atlantic","Pacific","Arctic"],"answer":"Pacific"},
        {"question":"Highest mountain?","options":["K2","Everest","Kilimanjaro","Fuji"],"answer":"Everest"},
        {"question":"River Ganga starts from?","options":["Gangotri","Yamunotri","Kedarnath","Badrinath"],"answer":"Gangotri"},
        {"question":"Capital of India?","options":["Mumbai","Delhi","Chennai","Kolkata"],"answer":"Delhi"},
        {"question":"Desert in Africa?","options":["Thar","Gobi","Sahara","Kalahari"],"answer":"Sahara"},
        {"question":"Smallest continent?","options":["Asia","Europe","Australia","Africa"],"answer":"Australia"},
        {"question":"Longest river?","options":["Amazon","Nile","Yangtze","Ganga"],"answer":"Nile"},
        {"question":"Taj Mahal city?","options":["Delhi","Agra","Jaipur","Lucknow"],"answer":"Agra"},
        {"question":"Pole Star direction?","options":["South","East","West","North"],"answer":"North"},
        {"question":"Island nation?","options":["India","Japan","China","Russia"],"answer":"Japan"}
    ],

    "sports": [
        {"question":"Cricket world cup 2011 winner?","options":["India","Aus","Eng","SA"],"answer":"India"},
        {"question":"Hockey national game of India?","options":["Yes","No"],"answer":"No"},
        {"question":"Olympics held every?","options":["2","3","4","5"],"answer":"4"},
        {"question":"Football legend?","options":["Messi","Jordan","Bolt","Nadal"],"answer":"Messi"},
        {"question":"Tennis grand slam?","options":["4","5","6","7"],"answer":"4"},
        {"question":"Badminton star of India?","options":["Saina","Dhoni","Kohli","Kapil"],"answer":"Saina"},
        {"question":"100m fastest man?","options":["Bolt","Gatlin","Lewis","Blake"],"answer":"Bolt"},
        {"question":"IPL team CSK city?","options":["Delhi","Mumbai","Chennai","Kolkata"],"answer":"Chennai"},
        {"question":"Kabaddi origin?","options":["India","China","Japan","Korea"],"answer":"India"},
        {"question":"Chess world champion?","options":["Anand","Carlsen","Kasparov","Fischer"],"answer":"Carlsen"}
    ]
}

@app.post("/generate-quiz", response_model=QuizResponse)
def generate_quiz(req: QuizRequest):
    topic = req.topic.lower()
    num = req.num_questions
    if topic not in QUESTION_BANK:
        return {"topic": topic, "quiz": []}

    questions = QUESTION_BANK[topic]
    if num > len(questions):
        num = len(questions)
    quiz_sample = random.sample(questions, num)
    return {"topic": topic, "quiz": quiz_sample}
