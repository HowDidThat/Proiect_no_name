import os


from groq import Groq


client = Groq(
    api_key="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",
)


chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Give me a python list with elements '[5,6,7]'",
        }
    ],
    model="llama3-8b-8192",
)
print(chat_completion.choices[0].message.content)