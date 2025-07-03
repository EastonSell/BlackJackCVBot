# 🧑‍💼 Boss-Agent Master Prompt  ─ Project Coordination Template
> **Purpose** Create a shared workspace where many specialist agents (✔ Implementation, 🧪 Testing, 📚 Docs, 📈 DevOps, etc.) can work in parallel, update their own status, and report to this single file the boss agent reviews.

---

## 1. Project Overview
* **Project Name:** ▲ EDIT HERE  
* **High-Level Goal (one sentence):** ▲ EDIT HERE  
* **Definition of “Done”:**  
  ```text
  • Feature-complete ✅
  • All unit + integration tests passing ✅
  • CI/CD pipeline green ✅
  • Documentation published ✅
```

* **Deadline / Milestones:**

  | Milestone                | Target Date | Owner | Status |
  | ------------------------ | ----------- | ----- | ------ |
  | Prototype skeleton       | ▲           | ▲     | ⬜ 0 %  |
  | Core feature set         | ▲           | ▲     | ⬜ 0 %  |
  | Test coverage ≥ 90 %     | ▲           | ▲     | ⬜ 0 %  |
  | First staging deployment | ▲           | ▲     | ⬜ 0 %  |
  | Final review & hand-off  | ▲           | ▲     | ⬜ 0 %  |

---

## 2. Task Breakdown (Kanban-style)

Update **one row per task**.
Progress bar legend → ⬜ 0 % · ▣ 25 % · ◧ 50 % · ◩ 75 % · ■ 100 %

| ID   | Description                 | Owner         | Dependencies | Status | Notes |
| ---- | --------------------------- | ------------- | ------------ | ------ | ----- |
| T-01 | Set up repo & CI            | DevOps-Agent  | none         | ⬜ 0 %  | ▲     |
| T-02 | Design API schema           | Lead-Dev      | T-01         | ⬜ 0 %  | ▲     |
| T-03 | Implement endpoint `/users` | Backend-Agent | T-02         | ⬜ 0 %  | ▲     |
| T-04 | Unit tests for `/users`     | QA-Agent      | T-03         | ⬜ 0 %  | ▲     |
| T-05 | Document TODO summary       | Docs-Agent    | none         | ▣ 25 % | - scanning repo for TODOs |
| …    | …                           | …             | …            | …      | …     |

> **How to update:**
>
> 1. Locate your row(s).
> 2. Change the status icon to show progress.
> 3. Append concise bullet notes if needed (keep ≤2 lines).

---

## 3. Branch / PR Tracker

| Branch                   | Purpose             | Latest Commit | PR # | Status |
| ------------------------ | ------------------- | ------------- | ---- | ------ |
| `feature/users-endpoint` | Implements `/users` | abc1234       | #17  | ◧ 50 % |
| ▲                        | ▲                   | ▲             | ▲    | ▲      |
| `work`                   | TODO summary docs   | 99b30b3       | N/A  | ▣ 25 % |

---

## 4. Decisions & Rationale Log

* **2025-07-03 · Architecture** – Chose FastAPI over Flask for async support. *(Lead-Dev)*
* **▲ DATE** – ▲ DECISION. *(Owner)*

---

## 5. Open Questions / Blockers

| #    | Question / Blocker                      | Assigned To  | Resolution Deadline | Status |
| ---- | --------------------------------------- | ------------ | ------------------- | ------ |
| Q-01 | Which cloud region fits latency target? | DevOps-Agent | ▲                   | ⬜ Open |
| ▲    | ▲                                       | ▲            | ▲                   | ▲      |

---

## 6. Daily Stand-Up (YYYY-MM-DD)

```text
🗓️ YYYY-MM-DD
What I did yesterday:  ▲
What I’m doing today:  ▲
Blockers:              ▲
```

(Each agent adds their own block; boss agent summarizes.)

```text
🗓️ 2025-07-03
What I did yesterday:  N/A
What I’m doing today:  Document TODO summary
Blockers:              None
```

---

## 7. Definition of Done Checklist

* [ ] All tasks in §2 show **■ 100 %**
* [ ] All milestones in §1 marked **Done**
* [ ] Code merged to `main` with green CI
* [ ] Docs generated & published
* [ ] Final demo approved by boss agent

---

## 8. Submission Instructions for Sub-Agents

1. **Never overwrite** another agent’s updates—merge thoughtfully.
2. Keep commit messages `feat/`, `fix/`, `doc/`, `chore/`, etc.
3. If you finish early, pick an unowned task or create a new one and assign yourself.
4. Ping the boss agent in this file when you hit 100 % on a task or need input.

---

> **Boss Agent Reminders**
>
> * Periodically collapse resolved questions, archive closed PRs, and prune completed tasks.
> * At EOD, post an **overall progress bar**:
>
>   ```text
>   Project completion ≈  ████████░░ 80 %
>   ```
