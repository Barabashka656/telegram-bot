import openai
from data.config import OPEN_AI_API_KEY

openai.api_key = OPEN_AI_API_KEY


def get_openai_response(text: str) -> str:
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=text,
        temperature=0.5,
        max_tokens=500,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
        stop=["You:"]
    )
    return response.get("choices")[0].get('text')
