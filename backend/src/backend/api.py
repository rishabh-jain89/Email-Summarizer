import os
import json
from fastapi import FastAPI
from pydantic import BaseModel
from .crew import build_crew
from .llm_wrapper import GeminiCrewAI
from fastapi.middleware.cors import CORSMiddleware
os.environ["CREWAI_TELEMETRY_ENABLED"] = "false"


class ChatRequest(BaseModel):
    context: str
    summary: dict
    question: str



app = FastAPI(title="Email Summarizer API", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailRequest(BaseModel):
    email_text: str

gemini_llm = GeminiCrewAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

import re
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

@app.post("/chat")
async def chat_with_email_context(request: Request):
    try:
        data = await request.json()

        variables = data.get("variables", {})
        inner_data = variables.get("data", {})
        messages = inner_data.get("messages", [])
        context_items = inner_data.get("context", [])

        user_question = ""
        for msg in reversed(messages):
            text_msg = msg.get("textMessage", {})
            if text_msg.get("role") == "user":
                user_question = text_msg.get("content", "")
                break

        email_text = ""
        summary = {}

        if isinstance(context_items, list):
            for c in context_items:
                desc = c.get("description")
                val = c.get("value", "")

                if desc == "emailText":
                    email_text = val
                elif desc == "summary":
                    try:
                        summary = json.loads(val)
                    except json.JSONDecodeError:
                        summary = {"raw": val}

        print(" Parsed question:", user_question)
        print(" Parsed email preview:", email_text[:80])
        print(" Parsed summary:", summary)

        if not user_question:
            return JSONResponse(content={
                "data": {
                    "generateCopilotResponse": {
                        "__typename": "CopilotResponse",
                        "messages": [
                            {
                                "__typename": "TextMessageOutput",
                                "role": "assistant",
                                "content": ["It looks like you didn't ask a question."]
                            }
                        ],
                        "status": {"__typename": "BaseResponseStatus", "code": "success"}
                    }
                }
            })


        crew = build_crew(mode="qa")
        for agent in crew.agents:
            agent.llm = gemini_llm

        raw_result = crew.kickoff(inputs={
            "email_text": email_text,
            "summary": summary,
            "question": user_question,
        })

        assistant_response = str(raw_result).strip() or "I couldn’t generate a useful answer."

        response = {
            "data": {
                "generateCopilotResponse": {
                    "__typename": "CopilotResponse",
                    "messages": [
                        {
                            "__typename": "TextMessageOutput",
                            "role": "assistant",
                            "content": [assistant_response]
                        }
                    ],
                    "status": {
                        "__typename": "BaseResponseStatus",
                        "code": "success"
                    }
                }
            }
        }

        return JSONResponse(content=response)

    except Exception as e:
        import traceback
        print(" Error in /chat:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/summarize")
def summarize_email(req: EmailRequest):
    crew = build_crew()

    for agent in crew.agents:
        agent.llm = gemini_llm

    raw_result= crew.kickoff(inputs={"email_text": req.email_text})
    raw_text = str(raw_result)
    cleaned = re.sub(r"^```(?:json)?|```$", "", raw_text.strip(), flags=re.MULTILINE).strip()

    try:
        summary = json.loads(str(cleaned))
    except json.JSONDecodeError:
        summary = {"raw_text": str(raw_text)}

    return {"summary": summary}

