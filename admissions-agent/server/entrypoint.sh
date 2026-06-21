#!/usr/bin/env bash
# Wire the writable dirs (clients/, kb/) onto the Railway persistent volume, then start the server.
# The agent (cwd=$AGENT_DIR) and the web layer both read/write clients/ and kb/; symlinking them to
# the volume makes that state survive container restarts.
set -euo pipefail

AGENT_DIR="${AGENT_DIR:-/app}"
DATA_DIR="${DATA_DIR:-/data}"

mkdir -p "$DATA_DIR/clients" "$DATA_DIR/kb"

# Seed the volume from the image baseline on first boot (idempotent).
if [ ! -e "$DATA_DIR/clients/_template" ] && [ -d "$AGENT_DIR/clients" ]; then
  cp -a "$AGENT_DIR/clients/." "$DATA_DIR/clients/" 2>/dev/null || true
fi
if [ -z "$(ls -A "$DATA_DIR/kb" 2>/dev/null || true)" ] && [ -d "$AGENT_DIR/kb" ]; then
  cp -a "$AGENT_DIR/kb/." "$DATA_DIR/kb/" 2>/dev/null || true
fi

# Replace the in-image dirs with symlinks to the volume (skip if already linked).
for d in clients kb; do
  if [ ! -L "$AGENT_DIR/$d" ]; then
    rm -rf "$AGENT_DIR/$d"
    ln -s "$DATA_DIR/$d" "$AGENT_DIR/$d"
  fi
done

cd "$AGENT_DIR"
exec uvicorn server.app:app --host 0.0.0.0 --port "${PORT:-8000}"
