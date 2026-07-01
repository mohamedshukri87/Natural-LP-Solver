from dotenv import load_dotenv
import os
from google import genai
import json
from pydantic import BaseModel
import logging


logging.basicConfig(filename="run.log", level=logging.INFO)
load_dotenv()

class Variable(BaseModel):
    variables: str

class Constraints(BaseModel):
    coefficients: dict[str, int]
    operator: str
    rhs: int


class Model(BaseModel):
    variables: list[str]
    objective: str
    objective_coefficients: dict[str, int]
    constraints: list[Constraints]

def use_ai(input):

    prompt = f"""
    You are a JSON extraction service.

    Extract the linear programming problem below.
    Return JSON in only the schema below
    Have the variables as a multi-letter word like Wheat (capitalised) be represented as wheat and not W,

    {{
    "variables": [],
    "objective": "",
    "objective_coefficients": {{}},
    "constraints": [
        {{
        "coefficients": {{}},
        "operator": "",
        "rhs": 0
        }}
    ]
    }}

    Problem:
    {input}
    """

    api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
        "response_mime_type": "application/json",
    }
    )


    text = response.text.replace("```json", "").replace("```", "").strip()

    try:
        model = Model.model_validate_json(text)
    except Exception as e:
        logging.error("AI has generated the wrong structure")
        raise ValueError(f"Invalid model: {e}")



    return response.text

