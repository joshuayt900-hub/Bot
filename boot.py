import os
import logging
from main import start_bot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logging.info("🚀 Boot-Datei gestartet")

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    logging.error("TOKEN fehlt → Bot stoppt")
    exit(1)

try:
    start_bot(TOKEN)
except Exception as e:
    logging.error(f"Boot Fehler: {type(e).__name__}: {e}")