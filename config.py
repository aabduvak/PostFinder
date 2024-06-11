import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
CHANNEL_ID = str(os.getenv("CHANNEL_ID"))
ADMIN_ID = str(os.getenv("ADMIN_ID"))
