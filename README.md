# 🤖 USARB Exam Prep Bot

> A Telegram bot for exam preparation at Universitatea de Stat Alecu Russo din Bălți (USARB).  
> Students can take discipline-specific quizzes, track their progress, and receive reminders before exams.

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-7.x-blue?logo=telegram)](https://core.telegram.org/bots/api)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Sprint](https://img.shields.io/badge/Sprint-2%20(current)-brightgreen)](#sprints)

---

## 📚 Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Bot Commands](#bot-commands)
- [Project Management](#project-management)
- [Sprints](#sprints)
- [Team](#team)

---

## About the Project

This bot was developed as part of the **Software Management** course at USARB.  
It simulates a real Agile project — from user story definition to sprint delivery — using Notion for project tracking and GitHub for source control.

**The problem it solves:** Students often approach exam sessions without a structured way to self-test. Professors have no feedback channel about where students are struggling. This bot bridges that gap directly inside Telegram — no extra apps required.

---

## Features

| Feature | Status | User Story |
|---|---|---|
| 🎯 Take a quiz (10 questions per discipline) | ✅ In Progress | US1 |
| ✍️ Professor adds/edits questions via bot | ✅ In Progress | US2 |
| 📊 Student views progress history | 🔄 Planned | US3 |
| 🔔 Exam reminders (3 days & 1 day before) | 📋 Backlog | US4 |
| 📈 Statistical reports for coordinators | 📋 Backlog | US5 |

---

## Architecture

```
usarb-quiz-bot/
├── bot/
│   ├── handlers/         # Telegram command & callback handlers
│   │   ├── student.py    # /start, /quiz, /progres
│   │   └── professor.py  # /adauga, /lista, /sterge
│   ├── db/               # Database layer
│   │   ├── models.py     # SQLAlchemy models
│   │   └── queries.py    # DB query helpers
│   └── utils/            # Shared utilities
│       ├── keyboards.py  # Inline keyboard builders
│       └── validators.py # Input validation
├── tests/                # Unit tests
├── docs/
│   └── sprints/          # Sprint notes and retrospectives
├── .env.example          # Environment variable template
├── main.py               # Entry point
└── requirements.txt
```

**Stack:**
- **Language:** Python 3.11
- **Bot framework:** `python-telegram-bot` v21
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **ORM:** SQLAlchemy
- **Deployment:** Webhook via ngrok (dev) / Railway (prod)

---

## Getting Started

### Prerequisites

- Python 3.11+
- A Telegram Bot token from [@BotFather](https://t.me/botfather)

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/your-org/usarb-quiz-bot.git
cd usarb-quiz-bot

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and fill in your BOT_TOKEN

# 5. Run
python main.py
```

### Environment Variables

```env
BOT_TOKEN=your_telegram_bot_token_here
DATABASE_URL=sqlite:///usarb_bot.db
WEBHOOK_URL=https://your-domain.com/webhook
DEBUG=True
```

---

## Bot Commands

### Student Commands

| Command | Description |
|---|---|
| `/start` | Welcome message and main menu |
| `/quiz` | Select a discipline and start a 10-question quiz |
| `/progres` | View your quiz history and scores |

### Professor Commands

| Command | Description |
|---|---|
| `/adauga` | Add a new question (guided step-by-step flow) |
| `/lista` | View all questions for your discipline |
| `/sterge <id>` | Delete a question by ID |
| `/editeaza <id>` | Edit an existing question |

---

## Project Management

This project is tracked in **Notion** using a Sprint Board.

- 📋 **Notion Board:** [Software Management Class (LP2)](https://notion.so)
- 🗂️ **User Stories:** US1–US5 (see [docs/user-stories.md](docs/user-stories.md))
- 🐛 **Bug Reports:** Use [GitHub Issues](.github/ISSUE_TEMPLATE/bug_report.md)
- ✨ **Feature Requests:** Use [GitHub Issues](.github/ISSUE_TEMPLATE/feature_request.md)

---

## Sprints

| Sprint | Period | Goal | Status |
|---|---|---|---|
| Sprint 0 — Setup | Apr 6–11 | Bot token, webhook, DB init, architecture | ✅ Done |
| Sprint 1 — US2 partial | Apr 12–25 | Professor adds questions (step-by-step flow) | 🔄 In Progress |
| Sprint 2 — US2 final + US1 partial | Apr 26–May 9 | Complete question management + quiz core | ▶️ Current |
| Sprint 3 — US1 final + US3 partial | May 10–23 | Quiz scoring, feedback, progress view | 📋 Planned |

See [`docs/sprints/`](docs/sprints/) for detailed sprint notes and retrospectives.

---

## Team

| Name | Role |
|---|---|
| Alina Borinschi | Developer / Scrum Master |
| Bogdan Jovmir | Developer |

---

## License

MIT — see [LICENSE](LICENSE) for details.
