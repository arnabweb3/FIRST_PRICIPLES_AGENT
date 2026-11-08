from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig

load_dotenv()

llm = genai.Client()

prompt = input("User : ")

def chatbot(prompt):
    response = llm.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents = prompt,
        config=GenerateContentConfig(
            temperature=0
        )
    )

    return response

response = chatbot(prompt=prompt)

print(f"Agent : {response.text}")
