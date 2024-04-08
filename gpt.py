
from openai import OpenAI
import os

client = OpenAI()
def main(prompt):

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    return(completion.choices[0].message.content)






