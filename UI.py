import json
import streamlit as st
import pandas as pd

user_input = []

text_questions = [
    "Start location",
    "End location",
    'Vibe',
    'Must-try activities',
    'Interests',
    'Additional information that could be helpul'
]

for question in text_questions:
    answer = st.text_input(question)
    user_input.append({question:answer})

print(user_input)