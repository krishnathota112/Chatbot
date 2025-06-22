import os
import google.generativeai as genai

# --- Configuration ---
# WARNING: Storing API keys directly in code is INSECURE and NOT recommended for production environments.
# This is for demonstration purposes ONLY.
# Replace 'YOUR_API_KEY_HERE' with the actual key you provided.
API_KEY = "AIzaSyCN4xdH5rljVIXvkIr5u1g2Bkwbaud3bXs" # Your key explicitly here

if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
    raise ValueError("API_KEY is not set. Please replace 'YOUR_API_KEY_HERE' with your actual key.")

genai.configure(api_key=API_KEY)

# Choose the Gemini 1.5 model. 'gemini-1.5-flash' is often preferred for chatbots due to speed and cost.
# You can also try 'gemini-1.5-pro' if your queries require more complex reasoning.
GEMINI_MODEL = 'gemini-1.5-flash' # Or 'gemini-1.5-pro'

# --- Chatbot Logic ---

def get_llm_response(user_query, chat_history=None):
    """
    Sends a user query to the Gemini LLM and gets a response.
    Includes a basic system instruction.
    """
    model = genai.GenerativeModel(GEMINI_MODEL)

    # Initialize chat session for multi-turn conversation
    # If chat_history is None, start a new chat. Otherwise, use the provided history.
    chat = model.start_chat(history=chat_history if chat_history is not None else [])

    # We provide system instructions as the very first message for models that support it,
    # or as context in the first user message if the model prefers.
    # For Gemini, it's often effective to set the persona in the initial user turn or through examples.
    # Here, we'll embed it into the first turn for simplicity.
    
    # Check if this is the very first turn to inject the system instruction
    if not chat.history:
        # Provide the persona as part of the first message to guide the model
        full_query = (
            "You are a helpful and polite customer support assistant for an e-commerce store called 'GadgetHub'. "
            "Your primary goal is to assist customers with their inquiries regarding orders, returns, and product information. "
            "If you cannot answer a question, politely suggest connecting them to a human agent and provide the contact phone number: 1-800-GADGET.\n\n"
            f"Customer query: {user_query}"
        )
    else:
        full_query = user_query # For subsequent turns, just send the user's message

    try:
        response = chat.send_message(full_query)
        # response.text contains the generated text
        return response.text, chat.history # Return response and updated history
    except Exception as e:
        # Check for specific quota errors
        if "quota" in str(e).lower():
            return f"Chatbot: I'm sorry, I've reached my usage limit for today. Please try again later or call us at 1-800-GADGET.", chat_history
        else:
            return f"Chatbot: An unexpected error occurred: {e}. Please try again later or contact a human agent.", chat_history

# --- Chatbot Interaction Loop ---
print("Welcome to GadgetHub's AI Customer Support! (Powered by Google Gemini 1.5)")
print("Type 'quit' to exit.")

current_chat_history = [] # To maintain conversation context

while True:
    user_message = input("You: ")
    if user_message.lower() == 'quit':
        print("Chatbot: Goodbye! Have a great day.")
        break
    
    response_text, updated_history = get_llm_response(user_message, current_chat_history)
    print(f"Chatbot: {response_text}")
    current_chat_history = updated_history # Update history for next turn