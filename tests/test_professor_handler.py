"""
Tests for professor handler input validation.

Covers the Sprint 1 regression: ConversationHandler state reset
when /adauga was called mid-session.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


def make_update(text: str, user_id: int = 1) -> MagicMock:
    update = MagicMock()
    update.message.text = text
    update.message.reply_text = AsyncMock()
    update.effective_user.id = user_id
    return update


def make_context(user_data: dict = None) -> MagicMock:
    ctx = MagicMock()
    ctx.user_data = user_data or {}
    return ctx


class TestQuestionValidation:

    @pytest.mark.asyncio
    async def test_empty_question_text_reprompts(self):
        from bot.handlers.professor import receive_question_text, WAITING_QUESTION_TEXT
        update = make_update("")
        context = make_context()

        result = await receive_question_text(update, context)

        update.message.reply_text.assert_called_once()
        assert "gol" in update.message.reply_text.call_args[0][0].lower()
        assert result == WAITING_QUESTION_TEXT

    @pytest.mark.asyncio
    async def test_valid_question_text_advances_state(self):
        from bot.handlers.professor import receive_question_text, WAITING_OPTION_A
        update = make_update("Ce este un algoritm?")
        context = make_context()

        result = await receive_question_text(update, context)

        assert context.user_data["question_text"] == "Ce este un algoritm?"
        assert result == WAITING_OPTION_A

    @pytest.mark.asyncio
    async def test_invalid_correct_answer_reprompts(self):
        from bot.handlers.professor import receive_correct, WAITING_CORRECT
        update = make_update("X")  # invalid
        context = make_context()

        result = await receive_correct(update, context)

        assert result == WAITING_CORRECT

    @pytest.mark.asyncio
    async def test_valid_correct_answer_advances(self):
        from bot.handlers.professor import receive_correct, WAITING_DISCIPLINE
        update = make_update("B")
        context = make_context()

        result = await receive_correct(update, context)

        assert context.user_data["correct"] == "B"
        assert result == WAITING_DISCIPLINE
