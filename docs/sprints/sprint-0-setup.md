# Sprint 0 — Setup

**Period:** April 6–11, 2026  
**Goal:** Get the project skeleton running — bot token, webhook, database, folder structure.  
**Status:** ✅ Complete (2/3 tasks done; Telegram config archived as duplicate)

---

## Sprint Goal

Establish the technical foundation so that feature development can begin in Sprint 1 without infrastructure blockers.

---

## Tasks

| Task | Assignee | Status | Notes |
|---|---|---|---|
| 🏛️ Arhitectura proiectului | Alina Borinschi | ✅ Done | Defined folder structure, chose `python-telegram-bot` v21 |
| 🗄️ Inițializare bază de date | Alina Borinschi | ✅ Done | SQLite with SQLAlchemy; 3 tables created |
| 🤖 Configurare bot Telegram (token, webhook) | Bogdan Jovmir | 🗃️ Archived | Merged into architecture task; webhook tested via ngrok |

**Completed:** 2/3 (the archived task was resolved as part of another task, not dropped)

---

## Decisions Made

- **Framework:** `python-telegram-bot` v21 (ConversationHandler for multi-step flows)
- **Database:** SQLite for development, plan to migrate to PostgreSQL before final demo
- **Deployment:** ngrok for local webhook during dev; Railway for production
- **Project tracking:** Notion sprint board (LP2)
- **Branch strategy:** `main` is protected; feature branches named `feature/US{n}-short-description`

---

## Database Schema (Initial)

```sql
CREATE TABLE questions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    discipline  TEXT NOT NULL,
    text        TEXT NOT NULL,
    option_a    TEXT NOT NULL,
    option_b    TEXT NOT NULL,
    option_c    TEXT NOT NULL,
    option_d    TEXT NOT NULL,
    correct     TEXT NOT NULL CHECK(correct IN ('A','B','C','D')),
    explanation TEXT,
    created_by  INTEGER,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active   BOOLEAN DEFAULT 1
);

CREATE TABLE users (
    telegram_id  INTEGER PRIMARY KEY,
    username     TEXT,
    role         TEXT DEFAULT 'student' CHECK(role IN ('student','professor')),
    discipline   TEXT,
    joined_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE quiz_sessions (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER REFERENCES users(telegram_id),
    discipline   TEXT NOT NULL,
    score        INTEGER,
    total        INTEGER,
    started_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
    finished_at  DATETIME
);
```

---

## Retrospective

**What went well:**
- Architecture decisions were quick — no major debates, everyone aligned on the stack
- SQLAlchemy schema was set up faster than expected

**What didn't go well:**
- Telegram webhook setup had a certificate issue with ngrok on Windows (resolved by switching to HTTP tunnel in dev mode)
- The "Configure bot" task was redundant — it overlapped with architecture setup

**Action for Sprint 1:**
- Be more granular when writing tasks so we don't create overlap
- Add a task for writing the first unit test (skipped this sprint)
