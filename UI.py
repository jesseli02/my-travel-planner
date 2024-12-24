import json
import streamlit as st
import pandas as pd
from together import Together as tg

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
    ['Interests', 'What are your general interests when traveling?', 'I enjoy walking around, trying new foods and exploring the culture', 'text', 'optional'],
    ['Trip Budget', 'Do you have a daily budget in mind', 'We plan to spend $2000 CAD total per person, excluding flights', 'text', 'optional'],
    ['Additional info', 'Is there anything else that would be good to know to help plan your trip itinerary?', 'I am a morning person', 'text', 'optional']
]
questions_table = pd.DataFrame(questions, columns=question_headers)

# Translate question table to UI on Streamlit
input_details = []

with st.form(key = 'submission_form'):
    key = 'submission_form',
    enter_to_submit = False,
    border = False,

    for question in questions_table.to_dict(orient ='records'):
        input_type = question['InputType']

        if input_type == 'text':
            answer = st.text_input(
                label = question['QuestionText'],
                placeholder = question['PlaceholderText']
            )
        elif input_type == 'date':
            answer = st.date_input(
                label=question['QuestionText']
            )
        elif input_type == 'time':
            answer = st.time_input(
                label=question['QuestionText'],
                step=1800
            )
        else:
            answer = None

        input_details.append({'question': question['QuestionName'], 'answer': answer})

    submitted = st.form_submit_button("Unleash the power of AI to generate my travel itinerary")

if submitted:

    #Call Together API
    client = tg(api_key="cbea512d1bf322aee99d7ce57605f76213a88036512f376396654844eba7efe8")

    prompt1 = "Could you help me plan a daily itinerary for my upcoming trip? Here are the details below: "

    # Format the trip_info as a readable string
    prompt2 = json.dumps(input_details)

    stream = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=[{"role": "user", "content": (prompt1 + prompt2)}],
        max_tokens=1000,
        stream=True
    )

    itinerary = ""

    st.write("Here's what I gathered from your travel input details:")
    st.write(stream)

# Button action to begin

# Get back model

# Print out user input details as summary

# Print out the model travel itinerary output



