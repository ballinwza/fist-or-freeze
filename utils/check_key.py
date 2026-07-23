import os
from dotenv import load_dotenv

load_dotenv()
    
def checking_env(key: str):
    token = os.getenv(key)

    print("--- Checking HF_TOKEN ---")
    if token:
        print(f"✅ Found : {token[:5]}...{token[-4:]} (Length: {len(token)})")
    else:
        print(f"❌ {key} is missing or None!")