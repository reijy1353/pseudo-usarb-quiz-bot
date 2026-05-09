# Sprint 2 — US2 Finalize + US1 Partial

**Period:** April 26 – May 9, 2026  
**Goal:** Complete question management (US2) and implement the core quiz flow (US1).  
**Status:** ▶️ Current Sprint

---

## Sprint Goal

By the end of this sprint:
1. Professors can fully manage questions (add, list, edit, delete)
2. Students can start a quiz, receive questions as inline buttons, and answer them

---

## User Story Reference

**US1 — Susținerea unui Quiz (partial)**
> Ca un student USARB, vreau să lansez un quiz de 10 întrebări cu variante multiple pentru o disciplină aleasă și să primesc scorul final cu explicații, astfel încât să identific lacunele de cunoaștere înainte de examen.

**Acceptance Criteria targeted this sprint:**
- [ ] Student selects discipline → receives first question in < 2 seconds
- [ ] Each question has 4 answer variants sent as Telegram inline buttons

**US2 — Adăugarea Întrebărilor (finalize)**
- [ ] Professor can view all questions with `/lista`
- [ ] Professor can edit/delete a question by ID

---

## Tasks

| Task | Assignee | Status | Description |
|---|---|---|---|
| 📋 Profesorul vede lista întrebărilor cu /lista | Bogdan Jovmir | 🔄 In Progress | Paginated list, shows ID + truncated question text + discipline |
| 🛑 Poate edita/șterge o întrebare prin ID | Bogdan Jovmir | 🔄 In Progress | `/sterge <id>`, confirmation prompt before delete |
| 🎓 Studentul selectează disciplina și primește prima întrebare în < 2s | Alina Borinschi | 🔄 In Progress | Inline keyboard with available disciplines |
| ⚪ Întrebările au 4 variante trimise ca butoane Telegram | Alina Borinschi | 🔄 In Progress | CallbackQueryHandler for A/B/C/D responses |

---

## Technical Notes

### Quiz Flow (US1)

```
/quiz
  └─ Inline keyboard: [Algoritmi] [Baze de Date] [POO] ...
        └─ Student picks discipline
              └─ Bot fetches 10 random questions from DB (shuffled)
                    └─ Sends question #1 with 4 inline buttons
                          └─ Student taps answer
                                └─ [Sprint 3] Feedback + next question
```

### /lista Pagination

Questions are paginated — 5 per page to avoid Telegram message length limits.  
Format:
```
[42] Baze de Date — Ce înseamnă JOIN în SQL?
[43] Algoritmi — Care este complexitatea QuickSort în cazul mediu?
...
```

### Fix Applied (from Sprint 1 blocker)

Resolved the ConversationHandler state reset by adding `per_user=True, per_chat=True` and wrapping the handler in a fresh `Application` instance. Added regression test in `tests/test_professor_handler.py`.

---

## Definition of Done (this sprint)

- [ ] Code reviewed and merged to `main`
- [ ] Manual test: professor adds 3 questions, lists them, deletes one
- [ ] Manual test: student selects discipline, receives question with 4 buttons
- [ ] No regressions in existing `/start` and `/adauga` commands
- [ ] Sprint notes updated in this file
