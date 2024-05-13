import os

from groq import Groq

chat_completion = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
).chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],
    model="mixtral-8x7b-32768",
)

