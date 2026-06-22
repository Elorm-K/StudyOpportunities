# Hugging Face Spaces image for the admissions-agent.
#
# HF Spaces (Docker SDK) builds the Dockerfile from the REPO ROOT, so this wrapper copies the
# admissions-agent/ subtree into /app. It mirrors admissions-agent/server/Dockerfile (the Railway
# image) with the COPY paths rebased to the repo root. The Railway path is unchanged on `main`;
# this file exists only on the huggingface-deploy branch.
#
# The Claude Agent SDK (Python) does NOT bundle the model runtime — it spawns the `claude` CLI,
# which must be on PATH. We install it from npm (@anthropic-ai/claude-code), which needs Node.

FROM python:3.12-slim

# --- Node 20 + the Claude Code CLI (the SDK shells out to `claude`) ---
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl ca-certificates git \
 && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
 && apt-get install -y --no-install-recommends nodejs \
 && npm install -g @anthropic-ai/claude-code \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python deps first (better layer caching)
COPY admissions-agent/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# The whole agent (CLAUDE.md, .claude/skills, lib, schema, intake, kb, clients/_template, server)
COPY admissions-agent/ /app/

ENV AGENT_DIR=/app \
    DATA_DIR=/data \
    APPROVAL_REQUIRED=true \
    PYTHONUNBUFFERED=1

# Verify the CLI is reachable at build time (fails the build early if the install path changed).
RUN claude --version

# HF Spaces routes external traffic to app_port (see README.md frontmatter). entrypoint.sh binds
# ${PORT:-8000}; we keep 8000 and declare app_port: 8000 in the Space README.
EXPOSE 8000
ENTRYPOINT ["/app/server/entrypoint.sh"]
