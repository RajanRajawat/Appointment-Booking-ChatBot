from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from src.chat.tools import register_user, verify_user, schedule_appointment, reschedule_appointment, cancel_appointment, view_appointments
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
from langgraph.checkpoint.memory import MemorySaver
import itertools




load_dotenv()



llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
# llm = ChatGroq(
#     model="llama-3.1-8b-instant",
#     temperature=0,
#     api_key=os.getenv("GROQ_API_KEY")
# )

tools = [register_user, verify_user, schedule_appointment, reschedule_appointment, cancel_appointment, view_appointments]


#- Tool Error Handler
@wrap_tool_call
def handle_tool_errors(request, handler):
    """Handle tool execution errors with custom messages."""
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({str(e)})",
            tool_call_id=request.tool_call["id"]
        )

system_promt_instructions = """
You are a friendly and helpful help desk assistant for WerqLabs Hospital.

Your responsibilities:
- Help users register and create an account
- Authenticate users using their mobile number and date of birth only once, if the user just created the account no need to verify again
- Assist users in booking doctor appointments
- Help reschedule or cancel existing appointments
- Help user get all his booked appointments
- Share only validated user's data.
- Answer simple, general health-related questions (basic guidance only, not medical diagnosis)

Guidelines:
- Always be polite, friendly, and conversational
- Ask for missing information step-by-step instead of assuming
- Before booking, rescheduling, or cancelling an appointment, ensure the user is verified
- If the user is not registered, guide them to register first
- If the user is not verified, ask them to verify their identity

Health-related behavior:
- Only answer general health questions (e.g., common cold, headache, basic precautions)
- Do NOT provide medical diagnosis or advanced medical advice
- If the user seems unwell, gently suggest booking an appointment with a doctor

Conversation strategy:
- Keep responses simple and clear
- Guide the user toward scheduling an appointment when appropriate
- Be proactive in helping but do not force actions
- Use available tools whenever required to complete tasks

You are not a doctor, but a smart assistant helping users connect with doctors.
"""


memory = MemorySaver()

agent = create_agent(llm, 
                     tools=tools,
                     system_prompt=system_promt_instructions,
                     checkpointer=memory,
                     middleware=[handle_tool_errors])




