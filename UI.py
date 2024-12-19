import json
import streamlit as st
import pandas as pd

# Create master list of questions

question_headers = ['QuestionName', 'QuestionText', 'PlaceholderText', 'InputType', 'Requirement']
questions = [
    ['Arrival location', 'Where are you starting your first day?', 'Brisbane, Australia', 'text', 'mandatory'],
    ['Departure location', 'Where are you leaving on your last day?', 'Melbourne, Australia', 'text', 'mandatory'],
    ['Arrival date', 'What date is your first day?', None , 'date', 'mandatory'],
    ['Departure date', 'What date is your last day?', None, 'date', 'mandatory'],
    ['Arrival time', 'What time do you start on your first day', None, 'time', 'optional'],
    ['Departure time', 'What time do you end on your last day', None, 'time', 'optional'],
    ['Travelers', 'How many people are you traveling with including yourself?', '2 couples, so 4 people in total', 'text', 'mandatory'],
    ['Activities in mind', 'Are there any activities/sites on your list that you want to visit', 'Sydney Opera House, Bondi Beach, See the Gold Coast', 'text', 'optional'],
    ['Travel style', 'Can you share anything about your travel style?', 'I try to avoid places where there are long line ups', 'text', 'optional'],
    ['Interests', 'What are your general interests when traveling?', 'I enjoy walking around, trying new foods and exploring the culture', ' text', 'optional'],
    ['Trip Budget', 'Do you have a daily budget in mind', 'We plan to spend $2000 CAD total per person, excluding flights', 'text', 'optional'],
    ['Additional info', 'Is there anything else that would be good for know to help plan your trip itinerary?', 'I am a morning person', 'text', 'optional']
]
questions_table = pd.DataFrame(questions, columns=question_headers)

# Translate question table to UI on Streamlit
input_details = []

for question in questions_table.to_dict(orient ='records'):
    match question['InputType']:
        case 'text':
            answer = st.text_input(
                label = question['QuestionText'],
                placeholder = 'E.g., ' + question['PlaceholderText']
            )
        case 'date':
            answer = st.date_input(
                label = question['QuestionText']
            )
        case 'time':
            answer = st.time_input(
                label = question['QuestionText'],
                step = 1800
            )
        case _:
            answer = None

    input_details.append({'question': question['QuestionName'], 'answer': answer})

# Create button UI to a generate itinerary
iteration = 0
def refresh(n):
    return n + 1

st.button(
    label = "Unleash the power of AI to generate my travel itinerary"
)
st.write(iteration)

# Button action to begin

# Get back model

# Print out user input details as summary

# Print out the model travel itinerary output



