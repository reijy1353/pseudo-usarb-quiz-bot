# User Stories

Format: **Ca un [tip utilizator], vreau să [acțiune], astfel încât să [beneficiu].**

---

## US1 — Susținerea unui Quiz ⭐ MVP

**Tip utilizator:** Student USARB  
**Story Points:** 8  
**Priority:** Must Have

> Ca un student USARB, vreau să lansez un quiz de 10 întrebări cu variante multiple pentru o disciplină aleasă și să primesc scorul final cu explicații, astfel încât să identific lacunele de cunoaștere înainte de examen.

### Acceptance Criteria

- [ ] Studentul selectează disciplina din meniu și botul trimite prima întrebare în < 2 secunde
- [ ] Fiecare întrebare are 4 variante de răspuns (A/B/C/D) trimise ca butoane Telegram
- [ ] După răspuns, botul indică dacă e corect/greșit și afișează explicația
- [ ] La final, botul afișează scorul (ex: 7/10) și lista întrebărilor greșite
- [ ] Quiz-ul poate fi reluat oricând, cu întrebări în ordine aleatorie

### Sprint Coverage

| Sprint | Tasks |
|---|---|
| Sprint 2 (partial) | Student selects discipline → receives first question with 4 buttons |
| Sprint 3 (final) | Correct/incorrect feedback, final score display, replay with shuffle |

---

## US2 — Adăugarea Întrebărilor ⭐ MVP

**Tip utilizator:** Profesor / Administrator Bot  
**Story Points:** 5  
**Priority:** Must Have

> Ca un profesor / administrator al botului, vreau să adaug o întrebare nouă cu 4 variante de răspuns și să o asignez unei discipline, astfel încât studenții să poată fi testați pe conținut actualizat.

### Acceptance Criteria

- [ ] Profesorul trimite `/adauga` și botul ghidează pas cu pas (întrebare → variante → răspuns corect → disciplină)
- [ ] Botul validează câmpurile obligatorii înainte de salvare — re-prompts pe input gol
- [ ] Întrebarea e atribuită disciplinei și devine activă imediat
- [ ] Profesorul poate vedea lista întrebărilor cu `/lista`
- [ ] Profesorul poate edita / șterge o întrebare prin ID

### Sprint Coverage

| Sprint | Tasks |
|---|---|
| Sprint 1 (partial) | `/adauga` flow, validation, discipline assignment |
| Sprint 2 (final) | `/lista`, `/sterge <id>`, `/editeaza <id>` |

---

## US3 — Vizualizarea Progresului ⭐ MVP

**Tip utilizator:** Student  
**Story Points:** 3  
**Priority:** Must Have

> Ca un student, vreau să văd istoricul quiz-urilor mele cu scoruri per disciplină, astfel încât să știu unde trebuie să mă concentrez mai mult.

### Acceptance Criteria

- [ ] `/progres` afișează scorurile ultimelor 10 sesiuni per disciplină
- [ ] Se evidențiază disciplinele cu scor mediu sub 50%
- [ ] Data și ora fiecărei sesiuni sunt vizibile

### Sprint Coverage

| Sprint | Tasks |
|---|---|
| Sprint 3 (partial) | `/progres` report per discipline |
| Sprint 4 (final, if needed) | Visual progress indicators, weak topic highlighting |

---

## US4 — Notificări și Remindere 🔵 Could Have

**Tip utilizator:** Student  
**Story Points:** 5  
**Priority:** Nice to Have

> Ca un student, vreau să primesc o notificare cu 3 zile și 1 zi înainte de examen, astfel încât să nu ratez sesiunile de pregătire.

### Acceptance Criteria

- [ ] Botul trimite automat mesaj cu 72h și 24h înainte de examen
- [ ] Notificarea include disciplina, data examenului și linkul către quiz
- [ ] Studentul poate dezactiva notificările cu `/notificari off`

---

## US5 — Rapoarte Statistice 🔵 Could Have

**Tip utilizator:** Coordonator Academic  
**Story Points:** 5  
**Priority:** Nice to Have

> Ca un coordonator academic, vreau să văd lunar câți studenți folosesc botul și care este rata de răspuns corect per disciplină, astfel încât să evaluez eficiența pregătirii.

### Acceptance Criteria

- [ ] `/raport` afișează numărul de sesiuni și utilizatori activi per lună
- [ ] Rata de răspuns corect per disciplină este vizibilă
- [ ] Datele pot fi exportate (CSV sau mesaj formatat)
