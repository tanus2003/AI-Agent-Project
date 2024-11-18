import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("")

if api_key:
    print(f"SerpAPI Key is set: {api_key[:5]}...")  # Print first 5 characters
else:
    print("SerpAPI Key is NOT set.")
