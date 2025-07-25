#!/bin/bash
pip install -r requirements.txt
playwright install
python visit_bot.py
