from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatMistralAI(
    api_key=os.getenv("MISTRAL_API_KEY"),
    model=os.getenv("MISTRAL_MODEL"),
    temperature=0.3
)


def generate_response(review, context, category, sentiment):
    """Generate a professional response for a submitted review."""
    prompt = (
        "You are S.A.G.E, a Support And Guidance Expert.\n\n"
        f"Review:\n{review}\n\n"
        f"Category:\n{category}\n\n"
        f"Sentiment:\n{sentiment}\n\n"
        f"Retrieved Policy Context:\n{context}\n\n"
        "Generate a professional response."
    )
    response = llm.invoke(prompt)
    return response.content


def generate_chat_response(message):
    """Generate a conversational reply for the S.A.G.E chatbot."""
    prompt = (
        "You are S.A.G.E (Support And Guidance Expert), a friendly and professional "
        "AI customer support chatbot. Answer the user's question helpfully and concisely.\n\n"
        f"User: {message}"
    )
    response = llm.invoke(prompt)
    return response.content