from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import pandas as pd
from textblob import TextBlob
import os
import json
import re

with open('responses.json', 'r') as f:
    responses = json.load(f)

app = Flask(__name__, template_folder=r"C:\Users\CWW\Desktop\Mental health chatbot\templates")
app.secret_key = 'your_secret_key'

excel_file = 'patient_data.xlsx'

if not os.path.exists(excel_file):
    df = pd.DataFrame(columns=[
        'Name', 'Age', 'Gender',
        'Q1', 'Q2', 'Q3', 'Q4', 'Q5',
        'Sentiment', 'Chat History'
    ])
    df.to_excel(excel_file, index=False)

@app.route('/')
def index():
    return redirect(url_for('form'))

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        session['name'] = request.form.get('name')
        session['age'] = request.form.get('age')
        session['gender'] = request.form.get('gender')
        return redirect(url_for('questionnaire'))
    return render_template('form.html')

@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    if request.method == 'POST':
        session['q1'] = request.form.get('q1')
        session['q2'] = request.form.get('q2')
        session['q3'] = request.form.get('q3')
        session['q4'] = request.form.get('q4')
        session['q5'] = request.form.get('q5')
        return redirect(url_for('chatbot'))

    patient_data = {
        'name': session.get('name'),
        'age': session.get('age'),
        'gender': session.get('gender')
    }
    return render_template('questionnaire.html', patient_data=patient_data)

def get_bot_response(user_input):
    user_input = user_input.lower()
    for category in responses:
        for keyword, response in responses[category].items():
            if re.search(r'\b' + re.escape(keyword) + r'\b', user_input):
                return response
    return "I'm here to listen. Please tell me more about how you're feeling."

@app.route('/chat', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST' and request.form.get('done') == 'true':
        return redirect(url_for('success'))

    user_input = request.form.get('user_input')
    if user_input:
        bot_response = get_bot_response(user_input)
        chat_log = session.get('chat_log', [])
        chat_log.append(f"You: {user_input}")
        chat_log.append(f"Bot: {bot_response}")
        session['chat_log'] = chat_log
        return jsonify({'response': bot_response})

    return render_template('chatbot.html')

@app.route('/success', methods=['GET'])
def success():
    name = session.get('name')
    age = session.get('age')
    gender = session.get('gender')
    q1, q2, q3, q4, q5 = session.get('q1'), session.get('q2'), session.get('q3'), session.get('q4'), session.get('q5')
    chat_history = "\n".join(session.get('chat_log', []))

    sentiment_text = TextBlob(chat_history).sentiment.polarity
    sentiment_label = "Positive" if sentiment_text > 0 else "Negative" if sentiment_text < 0 else "Neutral"

    df = pd.read_excel(excel_file)
    new_row = pd.DataFrame([{
        'Name': name,
        'Age': age,
        'Gender': gender,
        'Q1': q1, 'Q2': q2, 'Q3': q3, 'Q4': q4, 'Q5': q5,
        'Sentiment': sentiment_label,
        'Chat History': chat_history
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_excel(excel_file, index=False)

    return render_template('success.html', patient_data={'name': name})

if __name__ == '__main__':
    app.run(debug=True)
