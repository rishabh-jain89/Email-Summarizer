import os, json, re, traceback
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .crew import build_crew
from .llm_wrapper import GeminiCrewAI

os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

app = FastAPI(title="Email Summarizer API", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://email-summarizer-neon.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailRequest(BaseModel):
    email_text: str

gemini_llm = GeminiCrewAI(
    model="gemini-2.5-flash",
    temperature=0.2,
)

def format_response(message: str) -> dict:
    return {
        "data": {
            "generateCopilotResponse": {
                "__typename": "CopilotResponse",
                "messages": [
                    {"__typename": "TextMessageOutput", "role": "assistant", "content": [message]}
                ],
                "status": {"__typename": "BaseResponseStatus", "code": "success"},
            }
        }
    }



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

        if not user_question:
            return JSONResponse(content=format_response("Please ask a question about the email."))

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

        crew = build_crew(mode="qa")
        for agent in crew.agents:
            agent.llm = gemini_llm

        result = crew.kickoff(
            inputs={"email_text": email_text, "summary": summary, "question": user_question}
        )

        return JSONResponse(content=format_response(str(result).strip()))

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Server Error in /chat endpoint")


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

