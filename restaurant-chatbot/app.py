from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy restaurant info
restaurant_info = {
    "menu": "Our menu includes burgers, pizzas, pasta, salads, and desserts.",
    "hours": "We are open from 10 AM to 11 PM, Monday to Sunday.",
    "location": "We are located at 123 Main Street, Foodie City.",
    "contact": "You can call us at (123) 456-7890.",
    "specials": "Today's special is 'Grilled Chicken Alfredo'."
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message'].lower()
    response = "I'm sorry, I didn't understand that. Can you ask about menu, hours, location, contact, or specials?"

    if "menu" in user_message:
        response = restaurant_info["menu"]
    elif "hours" in user_message or "time" in user_message:
        response = restaurant_info["hours"]
    elif "location" in user_message or "address" in user_message:
        response = restaurant_info["location"]
    elif "contact" in user_message or "phone" in user_message:
        response = restaurant_info["contact"]
    elif "special" in user_message:
        response = restaurant_info["specials"]

    return render_template('chat.html', user_message=user_message, bot_response=response)

if __name__ == "__main__":
    app.run(debug=True)
