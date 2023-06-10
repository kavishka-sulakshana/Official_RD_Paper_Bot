import os
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_LINK_2 = os.getenv("WEBHOOK_PAPERS")
WEBHOOK_LINK_CMP = os.getenv("WEBHOOK_COMPS")
TOKEN = os.getenv("API_TOKEN")