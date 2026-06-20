import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logging.info("🚀 Boot gestartet")

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    logging.error("TOKEN fehlt → Stop")
    raise SystemExit(1)

try:
    from main import start_bot
    logging.info("📦 main.py geladen")
    start_bot(TOKEN)

except Exception as e:
    logging.error(f"❌ Crash im Boot: {type(e).__name__}: {e}")
    raise