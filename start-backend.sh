#!/bin/bash

# source "rivas-venv/bin/activate"
uvicorn WordNetEndpoint:app --host 0.0.0.0 --port 8000 --reload
