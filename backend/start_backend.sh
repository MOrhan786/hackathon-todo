#!/bin/bash
cd /mnt/d/main-hackathon-folder/hackathon2/phase-03-todo-list/backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
