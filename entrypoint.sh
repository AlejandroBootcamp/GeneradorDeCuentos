#!/usr/bin/env bash

export $(cat /app/.env | xargs)
python /app/. &
streamlit run /app/frontend/__main__.py