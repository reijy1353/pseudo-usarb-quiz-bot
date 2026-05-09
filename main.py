"""
USARB Exam Prep Bot — Entry Point
"""

import logging
import os
from dotenv import load_dotenv
from telegram.ext import Application

from bot.handlers.student import register_student_handlers
from bot.handlers.professor import register_professor_handlers
from bot.db.models import init_db

load_dotenv()

logging.basicConfig(
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN is not set in .env")

    init_db()
    logger.info("Database initialized.")

    app = Application.builder().token(token).build()

    register_student_handlers(app)
    register_professor_handlers(app)

    webhook_url = os.getenv("WEBHOOK_URL")
    if webhook_url:
        logger.info(f"Starting webhook at {webhook_url}")
        app.run_webhook(
            listen="0.0.0.0",
            port=int(os.getenv("PORT", 8443)),
            webhook_url=webhook_url,
        )
    else:
        logger.info("No WEBHOOK_URL set — starting in polling mode.")
        app.run_polling()


if __name__ == "__main__":
    main()
