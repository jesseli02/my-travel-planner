import json5 as json
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

with st.form(key = 'submission_form', enter_to_submit = False):
    for question in questions_table.to_dict(orient ='records'):
        input_type = question['InputType']

        if input_type == 'text':
            answer = st.text_input(
                label = question['QuestionText'],
                placeholder = question['PlaceholderText']
            )
        elif input_type == 'date':
            answer = str(
                    st.date_input(
                    label=question['QuestionText']
                )
            )
        elif input_type == 'time':
            answer = str(
                st.time_input(
                    label=question['QuestionText'],
                    step=1800
                )
            )
        else:
            answer = None

        input_details.append({'question': question['QuestionName'], 'answer': answer})

    submitted = st.form_submit_button("Unleash the power of AI to generate my travel itinerary")

if submitted:

    st.subheader("Your Travel Details")
    for item in input_details:
        st.markdown(f"**{item['question']}**: {item['answer']}")

    # Initialize the Together client
    try:
        client = tg(api_key="cbea512d1bf322aee99d7ce57605f76213a88036512f376396654844eba7efe8")
    except Exception as e:
        st.error(f"Failed to initialize Together client: {e}")
        st.stop()

    prompt1 = "Could you help me plan a daily itinerary for my upcoming trip? Here are the details below: "

    # Format the trip_info as a readable string
    prompt2 = json.dumps(input_details, indent = 2)
    full_prompt = prompt1 + prompt2

    # Call Together API without streaming
    try:
        stream = client.chat.completions.create(
            model = "meta-llama/Llama-3.3-70B-Instruct-Turbo",
            messages = [{"role": "user", "content": full_prompt}],
            max_tokens = 1000,
            stream = True
        )
        success = 1
    except Exception as e:
        st.error(f"API request failed: {e}")
        st.stop()

    if success == 1:
        st.success("Your travel itinerary has been generated!")
        st.markdown("### Generated Itinerary")
        for chunk in stream:
            st.markdown(chunk.choices[0].delta.content or "", end="", flush=True)
    else:
        st.warning("No itinerary was generated. Please check your inputs and try again.")