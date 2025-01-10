import json5 as json
import streamlit as st
import requests
import pandas as pd
from together import Together as tg

# Define the list of questions
questions = [
    {
        'QuestionName': 'Arrival location',
        'QuestionText': 'Where are you starting your first day?',
        'PlaceholderText': 'Brisbane, Australia',
        'InputType': 'text',
        'Requirement': 'mandatory'
    },
    {
        'QuestionName': 'Departure location',
        'QuestionText': 'Where are you leaving on your last day?',
        'PlaceholderText': 'Melbourne, Australia',
        'InputType': 'text',
        'Requirement': 'mandatory'
    },
    {
        'QuestionName': 'Arrival date',
        'QuestionText': 'What date is your first day?',
        'PlaceholderText': None,
        'InputType': 'date',
        'Requirement': 'mandatory'
    },
    {
        'QuestionName': 'Departure date',
        'QuestionText': 'What date is your last day?',
        'PlaceholderText': None,
        'InputType': 'date',
        'Requirement': 'mandatory'
    },
    {
        'QuestionName': 'Arrival time',
        'QuestionText': 'What time do you start on your first day?',
        'PlaceholderText': None,
        'InputType': 'time',
        'Requirement': 'optional'
    },
    {
        'QuestionName': 'Departure time',
        'QuestionText': 'What time do you end on your last day?',
        'PlaceholderText': None,
        'InputType': 'time',
        'Requirement': 'optional'
    },
    {
        'QuestionName': 'Travelers',
        'QuestionText': 'How many people are you traveling with including yourself?',
        'PlaceholderText': '2 couples, so 4 people in total',
        'InputType': 'text',
        'Requirement': 'mandatory'
    },
    {
        'QuestionName': 'Activities in mind',
        'QuestionText': 'Are there any particular activities/sites that you want to do or visit?',
        'PlaceholderText': 'Visit Sydney Opera House, Bondi Beach and see the Gold Coast',
        'InputType': 'text',
        'Requirement': 'optional'
    },
    {
        'QuestionName': 'Travel style',
        'QuestionText': 'Can you share anything about your travel style?',
        'PlaceholderText': 'I try to avoid places where there are long line ups',
        'InputType': 'text',
        'Requirement': 'optional'
    },
    {
        'QuestionName': 'Interests',
        'QuestionText': 'What are your general interests when traveling?',
        'PlaceholderText': 'I enjoy walking around, trying new foods and exploring the culture',
        'InputType': 'text',
        'Requirement': 'optional'
    },
    {
        'QuestionName': 'Trip Budget',
        'QuestionText': 'Do you have a daily budget in mind?',
        'PlaceholderText': 'We plan to spend $2000 CAD total per person, excluding flights',
        'InputType': 'text',
        'Requirement': 'optional'
    },
    {
        'QuestionName': 'Additional info',
        'QuestionText': 'Is there anything else that would be good to know to help plan your trip itinerary?',
        'PlaceholderText': 'I am a morning person',
        'InputType': 'text',
        'Requirement': 'optional'
    }
]

# Function to call TogetherAI's for initial submission
def form_submission(api_key, input_details):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {api_key}"
    }

    # Prepare the prompt by formatting user details
    prompt_intro = "Could you help me plan a daily itinerary for my upcoming trip? Here are the details below:\n"
    full_prompt = prompt_intro + json.dumps(input_details, indent = 2)
    payload = {
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "messages": [
            {
                "role": "user",
                "content": full_prompt
            }
        ],
        "max_tokens": 1000
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    content = data['choices'][0]['message']['content']
    return content

def handle_feedback(api_key, trip_details, itinerary, user_feedback):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {api_key}"
    }

    prompt_intro = "Could you help me revise my current trip itinerary based on the feedback below? \n"
    full_prompt = prompt_intro + user_feedback + "\nLatest itinerary version:\n" + itinerary
    payload = {
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "messages": [
            {
                "role": "user",
                "content": full_prompt
            }
        ],
        "max_tokens": 1000
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    content = data['choices'][0]['message']['content']
    return content

# UI start
st.title("Travel Itinerary Generator")

# Pre-defined variables
tg_api_key = "cbea512d1bf322aee99d7ce57605f76213a88036512f376396654844eba7efe8"

# Session states
if 'trip_details' not in st.session_state:
    st.session_state.trip_details = None

if 'itinerary' not in st.session_state:
    st.session_state.itinerary = []

if 'feedback_log' not in st.session_state:
    st.session_state.feedback_log = []

st.session_state.count = 0

# Create a form to collect user inputs
with st.form(key = 'submission_form', enter_to_submit = False):
    input_details = []

    for question in questions:
        input_type = question['InputType']
        question_text = question['QuestionText']
        placeholder = question['PlaceholderText']
        requirement = question['Requirement']

        # Create input widgets based on the InputType
        if input_type == 'text':
            answer = st.text_input(label = question_text, placeholder = placeholder, key = question['QuestionName'])
        elif input_type == 'date':
            answer = st.date_input(label = question_text, key = question['QuestionName'])
            answer = answer.strftime('%Y-%m-%d')  # Convert to string
        elif input_type == 'time':
            answer = st.time_input(label = question_text, key = question['QuestionName'], step=1800)  # 30-minute intervals
            answer = answer.strftime('%H:%M:%S')  # Convert to string
        else:
            answer = ""

        # Append the answer with its question name
        input_details.append({'question': question['QuestionName'], 'answer': answer})

    # Submit button
    submitted = st.form_submit_button(label = "Generate Itinerary", type = "primary")

# Action once submit button is clicked
if submitted:

    # Store trip details in session state
    st.session_state.trip_details = input_details

    # Display the entered travel details
    with st.expander("See your travel input details"):
        for item in input_details:
            st.markdown(f"**{item['question']}:** {item['answer']}")

    # Prepare and call the Together AI API to generate initial itinerary
    with st.spinner(text = "Generating your itinerary..."):
        itinerary = form_submission(api_key = tg_api_key, input_details = input_details)
    st.session_state.itinerary.append(itinerary)
    st.session_state.count = 1

# Display the generated itinerary
if st.session_state.count > 0:
    if st.session_state.count == 1:
        st.success("### Generated Itinerary")
        st.write(st.session_state.itinerary[-1])

# Feedback prompt
    with st.form (key = 'feedback_form', border = False):

        user_feedback = st.text_input(
            label = "\n***Please let me know if you'd like me to modify anything in your itinerary:***",
            placeholder = "Type your feedback here (e.g., Could you try to add small day-trip hike into the itinerary?):"
        )

        feedback_button = st.form_submit_button("Revise my itinerary")

    if feedback_button:
        with st.spinner(text = "Re-generating your itinerary..."):
            itinerary = handle_feedback(
                api_key = tg_api_key,
                trip_details = st.session_state.trip_details,
                itinerary = st.session_state.itinerary[-1],
                user_feedback = user_feedback
            )

            st.session_state.itinerary.append(itinerary)
            st.session_state.feedback_log.append(user_feedback)
            st.session_state.count += 1

        # Display revised itinerary
        st.success("### Revised Itinerary")
        st.write(st.session_state.itinerary[-1])




