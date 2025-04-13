from flask import Flask, render_template, request

app = Flask(__name__)

responses = {
    "hello": "Hello! How can I assist you today? I'm here to help with any questions about our Medical Center.",
    "hey": "Hey there! How can I help you today? Feel free to ask me anything about our Medical Center!",
    "hi": "Hi! I'm happy to help. What can I do for you today?",
    "greetings": "Hi there! How can I assist you today? Feel free to ask me anything about our Medical Center.",
    "timings": "Our Medical Center is open from 9 AM to 5 PM, Monday to Saturday. We are closed on Sundays.",
    "when are you open": "We're open from 9 AM to 5 PM, Monday to Saturday. Our doors are closed on Sundays.",
    "doctors": "We have General Physicians, Dentists, Pediatricians, and Gynecologists. Let me know if you'd like to know more about a specific doctor.",
    "appointment": "You can book an appointment by calling +123456789 or visiting our website at www.medcenter.com/appointments.",
    "location": "Our Medical Center is located at 123 Health Street, MedCity. We are easily accessible via public transport.",
    "contact": "You can contact us by calling +123456789, or emailing info@medcenter.com. We are also on social media!",
    "thank you": "You're welcome! If you need further assistance, just ask. I'm always here to help!",
    "thanks": "You're welcome! Feel free to ask if you have more questions.",
    "goodbye": "Goodbye! Take care, and we look forward to assisting you again soon.",
    "bye": "Goodbye! Wishing you all the best. Come back anytime!",
    "help": "You can ask me about: \n- Our opening hours\n- Information about our doctors\n- How to book an appointment\n- Our location and contact details.",
    "emergency": "If you need urgent care, please call our emergency hotline at +123456789. For life-threatening situations, dial your local emergency services.",
    "urgent care": "For urgent care, reach out to our emergency hotline at +123456789.",
    "services": "We offer health check-ups, dental care, pediatric care, gynecology, and much more.",
    "insurance": "We accept several insurance providers. For coverage details, please contact our billing department.",
    "facilities": "Our facilities include modern exam rooms, a dental clinic, a pediatric area, and an on-site pharmacy.",
    "feedback": "We'd love to hear your feedback! After your visit, please leave your comments via our website or directly at the reception.",
    "how are you": "I'm doing great, thanks for asking! How can I assist you today?",
    "what's your name": "I'm your Medical Center Chatbot! I'm here to help with all your questions.",
    "who are you": "I'm the Medical Center Chatbot, your digital assistant for all things related to our services and care.",
    "good day": "Good day to you too! How can I assist you today?"
}

@app.route("/", methods=["GET", "POST"])
def index():
    user_input = ""
    bot_response = ""
    if request.method == "POST":
        user_input = request.form["user_input"].lower()

        # Loop through the response dictionary and check if the user input contains any of the keys
        for key in responses:
            if key in user_input:
                bot_response = responses[key]
                break
        else:
            bot_response = "Sorry, I didn't understand that. Could you please rephrase?"

    return render_template("interface.html", user_input=user_input, bot_response=bot_response)

if __name__ == "__main__":
    app.run(debug=True)



