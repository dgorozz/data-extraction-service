from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv

from models import ModelOutput


load_dotenv()


GEMINI_MODEL_NAME = "gemini-2.5-flash"


# ================ SYSTEM PROMPT + MODEL ================
def get_system_prompt() -> str:
    with open("system-prompt.md", "r") as f:
        system_prompt = f.read()
    return system_prompt

prompt_template = ChatPromptTemplate(
    [
        SystemMessage(get_system_prompt()),
        ("user", "{user_input}"),
    ],
    input_variables=["user_input"]
)

model = ChatGoogleGenerativeAI(model=GEMINI_MODEL_NAME, temperature=0)
model = model.with_structured_output(
    schema=ModelOutput.model_json_schema(), 
    method="json_schema"
)
model = prompt_template | model


# ================ API ENDPOINTS ================
class UserInput(BaseModel):
    text: str

app = FastAPI()

@app.get("/")
def index():
    return JSONResponse(content={"status": "OK"}, status_code=200)

@app.post("/extract")
def extract(user_input: UserInput):
    extracted_data = model.invoke({"user_input": user_input.text})
    return JSONResponse(content=extracted_data, status_code=200)


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)
