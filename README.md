# Prompt Engineering Is Not System Design

A tiny, runnable demo showing why **LLM agents fail even when the model behaves correctly** and how system design (not better prompts) prevents it.

> The model wasn’t wrong.  
> The system let it guess.

---

## What this shows

A common agent failure mode:

- a tool returns *no data*
- the model infers meaning from the absence
- the system treats that inference as fact
- a destructive action is proposed (like deleting `.env`)

The reasoning is reasonable.  The system behavior is the problem.

---

## What’s in the repo
agent/ # proposes a plan (simulated model reasoning)

tools/ # return results with explicit uncertainty

executor/ # guardrails + execution control


---

## How it works

1. Tool searches for `.env` references → finds none  
2. Agent infers the file is unused and proposes deletion  
3. System validates the plan  
4. Action is **blocked or dry-run only**

Nothing is actually deleted.

---

## Run it

```bash
python -m demo.clean_repo


