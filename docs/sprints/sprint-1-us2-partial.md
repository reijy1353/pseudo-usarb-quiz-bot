# Sprint 1 — US2 Partial (Professor Adds Questions)

**Period:** April 12–25, 2026  
**Goal:** Implement the professor's question-adding flow (US2, partial).  
**Status:** 🔄 In Progress (0/3 tasks complete as of Apr 25)

---

## Sprint Goal

A professor should be able to send `/adauga` and be guided step-by-step through adding a new quiz question. The question must be validated before saving, assigned to a discipline, and immediately active.

---

## User Story Reference

**US2 — Adăugarea Întrebărilor**  
> Ca un profesor / administrator al botului, vreau să adaug o întrebare nouă cu 4 variante de răspuns, astfel încât studenții să poată fi testați pe conținut actualizat.

**Acceptance Criteria (from US2):**
- [ ] Professor sends `/adauga` → bot guides step by step (question → options → correct answer → discipline)
- [ ] Bot validates mandatory fields before saving — re-prompts on empty/invalid input
- [ ] Question is assigned to a discipline and becomes active immediately

---

## Tasks

| Task | Assignee | Status | Due |
|---|---|---|---|
| 👨‍🏫 Profesorul trimite /adauga și botul ghidează pas cu pas | Bogdan Jovmir | 🔄 In Progress | Apr 18 |
| ✅ Botul validează câmpurile obligatorii înainte de salvare | Alina Borinschi | 🔵 Not Started | Apr 21 |
| ❓ Întrebarea e atribuită disciplinei și devine activă imediat | Alina Borinschi | 🔄 In Progress | Apr 25 |

---

## Technical Notes

### ConversationHandler States

The `/adauga` flow uses `python-telegram-bot`'s `ConversationHandler`:

```
WAITING_QUESTION_TEXT → WAITING_OPTION_A → WAITING_OPTION_B 
→ WAITING_OPTION_C → WAITING_OPTION_D → WAITING_CORRECT 
→ WAITING_DISCIPLINE → CONFIRM → END
```

Each state validates input before transitioning. On empty input, the bot re-sends the same prompt.

### Known Issue (as of Apr 25)

ConversationHandler state resets unexpectedly if the professor sends `/adauga` while another session is still open. Under investigation — likely a missing `per_user=True` flag in handler config.

---

## Retrospective (Preliminary)

**Blocker:** The ConversationHandler bug slowed down Bogdan's task significantly. Discovered that `python-telegram-bot` v21 changed how nested handlers work compared to v13 — documentation wasn't updated for the new async API.

**Resolution plan:** Isolate the handler config, add a test case that reproduces the reset, fix before Sprint 2 begins.
