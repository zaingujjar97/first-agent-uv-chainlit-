import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import chainlit as cl

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in .env file.")

# Initialize OpenAI client and model
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Configuration for agent run
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Create agent
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model=model
)

# Handler for incoming messages
@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content.lower()

    # List of questions related to identity or ownership
    identity_questions = [
        "tum kon ho", "who are you", 
        "tumhe kisne banaya", "who made you", 
        "tumhara owner kon hai", "who is your owner", 
        "your creator", "your developer"
    ]

    # Check if the message contains identity/ownership-related questions
    if any(phrase in user_input for phrase in identity_questions):
        await cl.Message(content="I was created by Zain Gujjar, my boss").send()
    else:
        # Process the message through the agent
        result = await Runner.run(agent, message.content, run_config=config)
        await cl.Message(content=result.final_output).send()