# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### In Progress
- `/quiz` command: student selects discipline and receives first question
- Inline keyboard buttons (A/B/C/D) for answering
- Correct/incorrect feedback with explanation per question

---

## [0.2.0] — Sprint 2 (Apr 26 – May 9, 2026)

### Added
- `/lista` command: professor can view all questions for their discipline
- Edit and delete question by ID (`/sterge <id>`, `/editeaza <id>`)
- Student selects discipline from inline keyboard → receives first question in < 2s
- Questions delivered as Telegram inline buttons (4 options)

### Fixed
- Conversation handler state reset bug when professor sent `/adauga` mid-session
- Discipline assignment not persisting after bot restart (missing DB commit)

---

## [0.1.0] — Sprint 1 (Apr 12 – Apr 25, 2026)

### Added
- `/adauga` command: guided step-by-step flow for professors to add questions
  - Step 1: Enter question text
  - Step 2: Enter 4 answer options (A, B, C, D)
  - Step 3: Specify correct answer
  - Step 4: Assign to discipline
- Mandatory field validation before saving — bot prompts again on empty input
- Question saved to DB and becomes immediately active in the quiz pool

### Changed
- Switched from polling to webhook for better performance

---

## [0.0.1] — Sprint 0 (Apr 6 – Apr 11, 2026)

### Added
- Project architecture defined (handlers / db / utils structure)
- SQLite database initialized with `questions`, `users`, `quiz_sessions` tables
- Telegram bot token configured and webhook registered
- `/start` command returns welcome message
- Basic `.env` configuration with `BOT_TOKEN` and `DATABASE_URL`
- `requirements.txt` with initial dependencies
