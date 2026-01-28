import os
from dotenv import load_dotenv

load_dotenv()

# Site / environment
BASE_URL = os.getenv("BASE_URL", "https://projects.whiteweb.co.il/fattal-new/")
BROWSER = os.getenv("BROWSER", "chrome")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
TIMEOUT = int(os.getenv("TIMEOUT", "10"))

# HTTP Basic Auth (browser-level popup in test/staging)
# If your environment uses Basic Auth, set these in .env:
# BASIC_AUTH_USER=...
# BASIC_AUTH_PASSWORD=...
BASIC_AUTH_USER = os.getenv("BASIC_AUTH_USER")
BASIC_AUTH_PASSWORD = os.getenv("BASIC_AUTH_PASSWORD")
