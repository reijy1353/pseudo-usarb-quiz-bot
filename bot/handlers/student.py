"""
Student command handlers — US1: Susținerea unui Quiz
"""

import logging
import random
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ConversationHandler, ContextTypes
)
from bot.db.models import Session, Question, QuizSession, User

logger = logging.getLogger(__name__)

SELECTING_DISCIPLINE = 0
IN_QUIZ = 1

QUIZ_SIZE = 10


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/start — welcome message."""
    user = update.effective_user
    with Session() as session:
        existing = session.get(User, user.id)
        if not existing:
            session.add(User(telegram_id=user.id, username=user.username))
            session.commit()

    await update.message.reply_text(
        f"👋 Salut, *{user.first_name}*! Bine ai venit la *USARB Quiz Bot*.\n\n"
        "📚 Comenzi disponibile:\n"
        "• /quiz — Începe un quiz\n"
        "• /progres — Vezi progresul tău\n\n"
        "Succes la sesiune! 🎓",
        parse_mode="Markdown",
    )


async def quiz_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """/quiz — let the student pick a discipline."""
    with Session() as session:
        disciplines = (
            session.query(Question.discipline)
            .filter_by(is_active=True)
            .distinct()
            .all()
        )

    if not disciplines:
        await update.message.reply_text("⚠️ Nu există întrebări disponibile momentan.")
        return ConversationHandler.END

    discipline_names = [d[0] for d in disciplines]
    keyboard = [
        [InlineKeyboardButton(name, callback_data=f"discipline:{name}")]
        for name in discipline_names
    ]
    await update.message.reply_text(
        "📚 Alege disciplina pentru quiz:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return SELECTING_DISCIPLINE


async def discipline_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Student picked a discipline — load questions and send the first one."""
    query = update.callback_query
    await query.answer()

    discipline = query.data.split(":", 1)[1]

    with Session() as session:
        questions = (
            session.query(Question)
            .filter_by(discipline=discipline, is_active=True)
            .all()
        )

    if len(questions) < QUIZ_SIZE:
        await query.edit_message_text(
            f"⚠️ Disciplina *{discipline}* are doar {len(questions)} întrebări — "
            f"sunt necesare minim {QUIZ_SIZE}.",
            parse_mode="Markdown",
        )
        return ConversationHandler.END

    selected = random.sample(questions, QUIZ_SIZE)
    context.user_data["quiz"] = {
        "discipline": discipline,
        "questions": [q.id for q in selected],
        "index": 0,
        "score": 0,
        "wrong": [],
    }

    # Start DB session record
    with Session() as session:
        qs = QuizSession(
            user_id=query.from_user.id,
            discipline=discipline,
            total=QUIZ_SIZE,
        )
        session.add(qs)
        session.commit()
        context.user_data["quiz"]["session_id"] = qs.id

    await _send_question(query, context)
    return IN_QUIZ


async def _send_question(query_or_update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the current question with inline answer buttons."""
    quiz = context.user_data["quiz"]
    q_id = quiz["questions"][quiz["index"]]

    with Session() as session:
        q = session.get(Question, q_id)

    idx = quiz["index"] + 1
    keyboard = [
        [
            InlineKeyboardButton(f"A: {q.option_a}", callback_data=f"answer:A"),
            InlineKeyboardButton(f"B: {q.option_b}", callback_data=f"answer:B"),
        ],
        [
            InlineKeyboardButton(f"C: {q.option_c}", callback_data=f"answer:C"),
            InlineKeyboardButton(f"D: {q.option_d}", callback_data=f"answer:D"),
        ],
    ]
    text = f"❓ *Întrebarea {idx}/{QUIZ_SIZE}*\n\n{q.text}"

    if hasattr(query_or_update, "edit_message_text"):
        await query_or_update.edit_message_text(
            text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown"
        )
    else:
        await query_or_update.message.reply_text(
            text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown"
        )


async def answer_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Student answered — give feedback and advance."""
    query = update.callback_query
    await query.answer()

    answer = query.data.split(":", 1)[1]
    quiz = context.user_data["quiz"]
    q_id = quiz["questions"][quiz["index"]]

    with Session() as session:
        q = session.get(Question, q_id)

    if answer == q.correct:
        quiz["score"] += 1
        feedback = f"✅ *Corect!*\n\n_{q.explanation or 'Bine!'}_"
    else:
        quiz["wrong"].append(q.text)
        correct_text = getattr(q, f"option_{q.correct.lower()}")
        feedback = (
            f"❌ *Greșit.* Răspunsul corect era *{q.correct}: {correct_text}*\n\n"
            f"_{q.explanation or ''}_"
        )

    quiz["index"] += 1

    if quiz["index"] >= QUIZ_SIZE:
        # Quiz finished
        score = quiz["score"]
        wrong_list = quiz["wrong"]

        with Session() as session:
            qs = session.get(QuizSession, quiz["session_id"])
            if qs:
                qs.score = score
                qs.finished_at = datetime.utcnow()
                session.commit()

        wrong_text = ""
        if wrong_list:
            wrong_text = "\n\n*Întrebări greșite:*\n" + "\n".join(f"• {t[:80]}" for t in wrong_list)

        await query.edit_message_text(
            f"{feedback}\n\n"
            f"🏁 *Quiz terminat!*\n"
            f"Scor final: *{score}/{QUIZ_SIZE}*{wrong_text}\n\n"
            f"Trimite /quiz pentru a relua.",
            parse_mode="Markdown",
        )
        context.user_data.clear()
        return ConversationHandler.END

    await query.edit_message_text(feedback, parse_mode="Markdown")
    await _send_question(query, context)
    return IN_QUIZ


async def progres(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/progres — show quiz history. (US3 — Sprint 3)"""
    await update.message.reply_text(
        "📊 Funcționalitatea */progres* va fi disponibilă în Sprint 3.\n"
        "Rămâi pe fază! 🚀",
        parse_mode="Markdown",
    )


def register_student_handlers(app: Application) -> None:
    quiz_conv = ConversationHandler(
        entry_points=[CommandHandler("quiz", quiz_start)],
        states={
            SELECTING_DISCIPLINE: [
                CallbackQueryHandler(discipline_selected, pattern=r"^discipline:")
            ],
            IN_QUIZ: [
                CallbackQueryHandler(answer_received, pattern=r"^answer:")
            ],
        },
        fallbacks=[],
        per_user=True,
        per_chat=True,
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(quiz_conv)
    app.add_handler(CommandHandler("progres", progres))
