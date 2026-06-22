---
title: Admissions Agent
emoji: 🎓
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 8000
pinned: false
---

# Admissions Agent — Hugging Face Spaces deploy

This branch (`huggingface-deploy`) adds the files Hugging Face Spaces needs to build and run the
study-abroad admissions agent. The Railway deploy lives on `main` and is untouched.

The agent itself lives under [`admissions-agent/`](admissions-agent/). The HF-specific additions are:

- **`Dockerfile`** (repo root) — wrapper that builds `admissions-agent/` from the repo root, since
  HF builds the Dockerfile from root (mirror of `admissions-agent/server/Dockerfile`).
- **`.dockerignore`** (repo root) — keeps the image lean and excludes runtime client data.
- **This `README.md` frontmatter** — the Space config (`sdk: docker`, `app_port: 8000`).

## Deploy steps

1. Create a new **Docker** Space on Hugging Face (`huggingface.co/new-space` → SDK: Docker).
2. Add this branch as a remote and push it to the Space's `main`:
   ```bash
   git remote add hf https://huggingface.co/spaces/<your-username>/<space-name>
   git push hf huggingface-deploy:main
   ```
3. In the Space **Settings → Variables and secrets**, add:
   - `ANTHROPIC_API_KEY` (secret, **required** — no logged-in CLI on the Space)
   - optional overrides: `CLAUDE_MODEL`, `MAX_BUDGET_USD_INTAKE`, `MAX_BUDGET_USD_RESEARCH`,
     `MAX_TURNS`, `MAX_RUN_SECONDS_INTAKE`, `MAX_RUN_SECONDS_RESEARCH`, `MAX_CONCURRENT_RUNS`
   - **Report approval is OFF by default** (`APPROVAL_REQUIRED=false`): reports auto-release
     to the applicant. To require human approval instead, set `APPROVAL_REQUIRED=true` **and**
     `OPERATOR_TOKEN` (the operator approval endpoints are disabled without a token).
4. The Space builds the Dockerfile and serves on `app_port: 8000`. Public URL: `https://<username>-<space>.hf.space`.

## Notes / caveats

- **RAM:** the free CPU tier (≈16GB) comfortably runs the Opus `claude` CLI the agent spawns — this
  is why HF is a better free fit than Render/Koyeb's small free instances.
- **Storage is ephemeral on the free tier.** `DATA_DIR=/data` (client profiles, KB updates) resets
  on every rebuild/restart. Fine for testing; add a paid persistent disk for durable state.
- **Idle sleep:** free Spaces sleep after extended inactivity and wake on the next visit.
