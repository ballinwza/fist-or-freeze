from google import genai
from dotenv import load_dotenv

load_dotenv()


def check_avalible_model(key: str):
    client = genai.Client(api_key=key)

    print("=== Available Models ===")
    for model in client.models.list():
        print(f"Model ID: {model.name}")