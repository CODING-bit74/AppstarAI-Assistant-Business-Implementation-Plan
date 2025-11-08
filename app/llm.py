import os
from openai import OpenAI

# Get API key and model from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

client = None  # Initialize client as None

def get_llm_answer(question: str, context: str = "") -> str:
    """
    Uses OpenAI to generate a more intelligent answer when the initial search fails.
    If no API key is present, it returns a user-friendly message.
    """
    global client
    # Check if the API key is missing or invalid
    if not OPENAI_API_KEY or not OPENAI_API_KEY.startswith("sk-"):
        return (
            "I can answer questions about our services, pricing, and contact information. "
            "For more advanced questions, my AI capabilities are not yet configured. "
            "Please ask one of the questions from the menu, or type 'help'."
        )

    # Initialize the client only if the key is valid and the client doesn't exist
    if client is None:
        client = OpenAI(api_key=OPENAI_API_KEY)

    try:
        # Create a system message with context
        system_message = (
            "You are AppstarAI's Smart Assist, a helpful customer support chatbot. "
            "Your goal is to provide friendly, professional, and accurate answers. "
            "When a user's question doesn't have a predefined answer, you'll generate one."
        )
        if context:
            system_message += f"\n\n**Context:**\n{context}"

        # Create a user message
        user_message = f"**User's Question:**\n{question}"

        # Call the OpenAI API
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            max_tokens=250,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        # Log the error for debugging, but return a friendly message to the user
        print(f"OpenAI API error: {e}")
        return "Sorry, I'm having a little trouble connecting to my advanced AI. Please try again in a moment."