import openai
from bot.data.config import OPEN_AI_API_KEY

openai.api_key = OPEN_AI_API_KEY


def get_openai_response(user_input: str, messages: list) -> list:
    messages = update(messages, "user", user_input)
    response = get_response(messages)
    messages = update(messages, 'assistant', response)
    return messages

def update(messages: list, role, content):
    messages.append({'role': role, 'content': content})
    return messages

def get_response(messages):
   
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages,
    )
    return response.get('choices')[0].get('message').get('content')
