import json5 as json
import streamlit as st
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
        'QuestionText': 'Are there any activities/sites on your list that you want to visit?',
        'PlaceholderText': 'Sydney Opera House, Bondi Beach, See the Gold Coast',
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


# Function to call TogetherAI's
def generate_itinerary(api_key, prompt):
    try:
        # Initialize the TogetherAI client with your API key
        client = tg(api_key=api_key)

        # Call the TogetherAI API with streaming enabled
        stream = client.chat.completions.create(
            model = "meta-llama/Llama-3.3-70B-Instruct-Turbo",  # Ensure this is the correct model name
            messages = [{"role": "user", "content": prompt}],
            max_tokens = 1000,
            response_format = {"type": "string"},
            stream = False
        )
        return stream
    except Exception:
        st.error("API request failed")
        return None

input_details = []
# Create a form to collect user inputs
with st.form(key='submission_form', enter_to_submit = False):
    for question in questions:
        input_type = question['InputType']
        question_text = question['QuestionText']
        placeholder = question['PlaceholderText']

        # Create input widgets based on the InputType
        if input_type == 'text':
            answer = st.text_input(label=question_text, placeholder=placeholder)
        elif input_type == 'date':
            answer = st.date_input(label=question_text)
            answer = answer.strftime('%Y-%m-%d')  # Convert to string
        elif input_type == 'time':
            answer = st.time_input(label=question_text, step=1800)  # 30-minute intervals
            answer = answer.strftime('%H:%M:%S')  # Convert to string
        else:
            answer = ""

        # Append the answer with its question name
        input_details.append({'question': question['QuestionName'], 'answer': answer})

    # Submit button
    submitted = st.form_submit_button("Generate Itinerary")

if submitted:
    # Display the entered travel details
    st.subheader("Your Travel Details")
    for item in input_details:
        st.markdown(f"{item['question']}: {item['answer']}")

    # Prepare the prompt for the API
    prompt1 = "Could you help me plan a daily itinerary for my upcoming trip? Here are the details below:\n"
    prompt2 = json.dumps(input_details, indent=2)
    full_prompt = prompt1 + prompt2

    # Call the TogetherAI API
    api_key = "cbea512d1bf322aee99d7ce57605f76213a88036512f376396654844eba7efe8"  # Replace with your API key or use st.secrets
    itinerary = generate_itinerary(api_key, full_prompt)

    if itinerary:
        st.success("Success! Your travel itinerary has been generated!")
        st.markdown("### Generated Itinerary")
        st.write(itinerary)

    else:
        st.warning("No itinerary was generated. Please check your inputs and try again.")

