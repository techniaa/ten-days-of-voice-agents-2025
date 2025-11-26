# backend/src/agent.py – Zerodha SDR Agent (Day 5 Primary + Advanced)
import json
import os
import asyncio
from datetime import datetime
from typing import Annotated, Optional
from dataclasses import dataclass, field

from dotenv import load_dotenv
load_dotenv(".env.local")

from livekit.agents import (
    Agent, AgentSession, JobContext, JobProcess,
    RoomInputOptions, WorkerOptions, cli,
    function_tool, RunContext
)
from livekit.plugins import murf, deepgram, google, silero, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

# Load Zerodha FAQ
FAQ_FILE = "shared-data/zerodha_faq.json"
with open(FAQ_FILE, "r", encoding="utf-8") as f:
    ZERODHA_FAQ = json.load(f)["faq"]

# Demo Slots
AVAILABLE_SLOTS = [
    "Tomorrow at 10:00 AM IST — Kite Demo",
    "Tomorrow at 4:00 PM IST — Account Setup Assistance",
    "Day after at 11:30 AM IST — Beginners Stock Training",
]

@dataclass
class Lead:
    name: str = ""
    email: str = ""
    trading_experience: str = ""
    investment_interest: str = ""
    booked_slot: str = ""

@dataclass
class UserData:
    lead: Lead = field(default_factory=Lead)
    session: Optional[AgentSession] = None

def save_lead(lead: Lead):
    os.makedirs("leads", exist_ok=True)
    data = {
        "timestamp": datetime.now().isoformat(),
        "name": lead.name,
        "email": lead.email,
        "trading_experience": lead.trading_experience,
        "investment_interest": lead.investment_interest,
        "booked_slot": lead.booked_slot or "Not booked"
    }
    with open("leads/zerodha_leads.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")

    # Create email draft
    email_draft = {
        "subject": f"Welcome to Zerodha, {lead.name.split()[0] if lead.name else 'there'}!",
        "body": f"Hi {lead.name.split()[0] if lead.name else 'there'},\n\n"
                f"Thanks for connecting! You mentioned interest in "
                f"{lead.investment_interest or 'starting your investment journey'}.\n\n"
                f"I have tentatively kept a demo session slot:\n"
                f"→ {lead.booked_slot or 'Pick your preferred time'}\n\n"
                f"We’ll help you invest confidently with Zerodha.\n\n"
                f"Regards,\nAayush\nClient Education Specialist @ Zerodha"
    }
    os.makedirs("email_drafts", exist_ok=True)
    with open(f"email_drafts/{lead.email or 'unknown'}_{int(datetime.now().timestamp())}.json", "w") as f:
        json.dump(email_draft, f, indent=2)

    print("\nLEAD SAVED + EMAIL DRAFT CREATED!\n")
    print(data)

@function_tool
async def answer_zerodha_question(ctx: RunContext[UserData], question: Annotated[str, "User question about Zerodha"]) -> str:
    q = question.lower()
    for item in ZERODHA_FAQ:
        if any(word in q for word in item["q"].lower().split()):
            return item["a"]
    return "Zerodha is India’s biggest stock broker with low brokerage and powerful trading tools like Kite and Coin. Would you like help starting your trading journey?"

@function_tool
async def collect_lead_field(ctx: RunContext[UserData], field: Annotated[str, "name/email/trading_experience/investment_interest"]) -> str:
    field = field.strip().lower()
    if field not in {"name", "email", "trading_experience", "investment_interest"}:
        return "I can collect: name, email, trading experience, and investment interest."

    await ctx.userdata.session.say(f"Sure! What's your {field.replace('_', ' ')}?")
    return f"Asking for {field}..."

@function_tool
async def show_slots(ctx: RunContext[UserData]) -> str:
    return "\n".join([f"{i+1}. {slot}" for i, slot in enumerate(AVAILABLE_SLOTS)])

@function_tool
async def book_slot(ctx: RunContext[UserData], index: Annotated[int, "1-3"]) -> str:
    if 1 <= index <= len(AVAILABLE_SLOTS):
        slot = AVAILABLE_SLOTS[index - 1]
        ctx.userdata.lead.booked_slot = slot
        save_lead(ctx.userdata.lead)
        return f"Booked! You’re confirmed for:\n{slot}\nWe’ll help you start investing confidently."
    return "Invalid choice! Please say a number between 1 and 3."

class ZerodhaSDR(Agent):
    def __init__(self):
        super().__init__(
            instructions="""
You are Aayush from Zerodha Client Education Team.
Act as a friendly financial guide.

Your goals:
- Understand if user is new or experienced trader
- Answer Zerodha questions from the FAQ
- Collect: name, email, trading experience, investment interest
- Offer to book a demo or account opening help

Use a simple, confident tone. Avoid market advice.
""",
            tools=[answer_zerodha_question, collect_lead_field, show_slots, book_slot]
        )

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()

async def entrypoint(ctx: JobContext):
    userdata = UserData()

    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-2.5-flash"),
        tts=murf.TTS(voice="en-IN-priya", style="Friendly"),
        vad=ctx.proc.userdata["vad"],
        turn_detection=MultilingualModel(),
        userdata=userdata,
    )
    userdata.session = session

    await session.start(
        agent=ZerodhaSDR(),
        room=ctx.room,
        room_input_options=RoomInputOptions(noise_cancellation=noise_cancellation.BVC()),
    )
    
    await ctx.connect(auto_subscribe=True)
    await asyncio.sleep(1)

    await session.say(
        "Hi! This is Aayush from Zerodha. Welcome! Are you planning to start investing in stocks or mutual funds? I can guide you through a smooth account opening!",
        allow_interruptions=True,
    )

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
