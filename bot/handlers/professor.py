"""
Professor command handlers — US2: Adăugarea / Gestionarea Întrebărilor
"""

import logging
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ConversationHandler, filters, ContextTypes
)
from bot.db.models import Session, Question

logger = logging.getLogger(__name__)

# ConversationHandler states
(
    WAITING_QUESTION_TEXT,
    WAITING_OPTION_A,
    WAITING_OPTION_B,
    WAITING_OPTION_C,
    WAITING_OPTION_D,
    WAITING_CORRECT,
    WAITING_DISCIPLINE,
) = range(7)


async def adauga_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Entry point for /adauga — begins the question-adding flow."""
    await update.message.reply_text(
        "✍️ *Adaugă o întrebare nouă*\n\n"
        "Pas 1/7 — Scrie textul întrebării:",
        parse_mode="Markdown",
    )
    return WAITING_QUESTION_TEXT


async def receive_question_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    if not text:
        await update.message.reply_text("⚠️ Textul întrebării nu poate fi gol. Încearcă din nou:")
        return WAITING_QUESTION_TEXT

    context.user_data["question_text"] = text
    await update.message.reply_text("Pas 2/7 — Varianta *A*:", parse_mode="Markdown")
    return WAITING_OPTION_A


async def receive_option(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Generic handler for options A–D."""
    text = update.message.text.strip()
    state = context.user_data.get("_awaiting_option")

    if not text:
        await update.message.reply_text(f"⚠️ Varianta nu poate fi goală. Încearcă din nou:")
        return state  # Re-ask same state

    context.user_data[f"option_{state.lower()}"] = text

    next_map = {
        "A": (WAITING_OPTION_B, "B", "3"),
        "B": (WAITING_OPTION_C, "C", "4"),
        "C": (WAITING_OPTION_D, "D", "5"),
        "D": (WAITING_CORRECT, None, "6"),
    }
    next_state, next_letter, step = next_map[state]

    if next_letter:
        await update.message.reply_text(
            f"Pas {step}/7 — Varianta *{next_letter}*:", parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "Pas 6/7 — Care este răspunsul corect? Trimite *A*, *B*, *C* sau *D*:",
            parse_mode="Markdown",
        )

    return next_state


async def receive_option_a(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["_awaiting_option"] = "A"
    return await receive_option(update, context)


async def receive_option_b(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["_awaiting_option"] = "B"
    return await receive_option(update, context)


async def receive_option_c(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["_awaiting_option"] = "C"
    return await receive_option(update, context)


async def receive_option_d(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["_awaiting_option"] = "D"
    return await receive_option(update, context)


async def receive_correct(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    answer = update.message.text.strip().upper()
    if answer not in ("A", "B", "C", "D"):
        await update.message.reply_text("⚠️ Trimite doar A, B, C sau D:")
        return WAITING_CORRECT

    context.user_data["correct"] = answer
    await update.message.reply_text(
        "Pas 7/7 — Disciplina (ex: *Algoritmi*, *Baze de Date*, *POO*):",
        parse_mode="Markdown",
    )
    return WAITING_DISCIPLINE


async def receive_discipline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    discipline = update.message.text.strip()
    if not discipline:
        await update.message.reply_text("⚠️ Disciplina nu poate fi goală:")
        return WAITING_DISCIPLINE

    data = context.user_data
    with Session() as session:
        q = Question(
            text=data["question_text"],
            option_a=data["option_a"],
            option_b=data["option_b"],
            option_c=data["option_c"],
            option_d=data["option_d"],
            correct=data["correct"],
            discipline=discipline,
            created_by=update.effective_user.id,
        )
        session.add(q)
        session.commit()
        question_id = q.id

    await update.message.reply_text(
        f"✅ Întrebarea a fost salvată cu ID *#{question_id}* la disciplina *{discipline}*.\n\n"
        f"Folosește /adauga pentru a adăuga alta sau /lista pentru a vedea toate.",
        parse_mode="Markdown",
    )
    context.user_data.clear()
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ Operațiune anulată.")
    context.user_data.clear()
    return ConversationHandler.END


async def lista(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/lista — show all questions for the professor's discipline."""
    with Session() as session:
        questions = session.query(Question).filter_by(is_active=True).order_by(Question.id).all()

    if not questions:
        await update.message.reply_text("Nu există întrebări în baza de date.")
        return

    # Paginate: 5 per message
    pages = [questions[i:i + 5] for i in range(0, len(questions), 5)]
    for page in pages:
        lines = []
        for q in page:
            truncated = q.text[:60] + "..." if len(q.text) > 60 else q.text
            lines.append(f"[{q.id}] {q.discipline} — {truncated}")
        await update.message.reply_text("\n".join(lines))


async def sterge(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/sterge <id> — delete a question by ID."""
    args = context.args
    if not args or not args[0].isdigit():
        await update.message.reply_text("Folosire: /sterge <id>")
        return

    question_id = int(args[0])
    with Session() as session:
        q = session.get(Question, question_id)
        if not q:
            await update.message.reply_text(f"⚠️ Nu există întrebarea cu ID #{question_id}.")
            return
        q.is_active = False
        session.commit()

    await update.message.reply_text(f"🗑️ Întrebarea #{question_id} a fost ștearsă.")


def register_professor_handlers(app: Application) -> None:
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("adauga", adauga_start)],
        states={
            WAITING_QUESTION_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_question_text)],
            WAITING_OPTION_A: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_option_a)],
            WAITING_OPTION_B: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_option_b)],
            WAITING_OPTION_C: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_option_c)],
            WAITING_OPTION_D: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_option_d)],
            WAITING_CORRECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_correct)],
            WAITING_DISCIPLINE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_discipline)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_user=True,
        per_chat=True,
    )
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("lista", lista))
    app.add_handler(CommandHandler("sterge", sterge))
