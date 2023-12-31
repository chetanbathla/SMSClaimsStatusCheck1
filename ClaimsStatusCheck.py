from azure.communication.chat import ChatClient
from twilio.rest import Client
import openai

# Set up Azure Communication Services
endpoint = "https://claimsstatuscommservice.communication.azure.com"  # Replace with your Azure Communication Services endpoint
access_key = "xMdYfkRk71R0Rr7IBCgc4GKzKr1PWxEBzs3EseQSaEKMVxr0hjXET47aMBMDZGn+vQ7r1+xjXCVxVC3+7sc1tg=="  # Replace with your Azure Communication Services access key
chat_client = ChatClient(endpoint, access_key)

# Set up Twilio
account_sid = "ACd9a2cfc0ad4f0235c94c717d2bf9f33a"  # Replace with your Twilio account SID
auth_token = "0da96bf84014f9e91e8d420eb0533888"  # Replace with your Twilio auth token
twilio_phone_number = "+18559654331"  # Replace with your Twilio phone number
twilio_client = Client(account_sid, auth_token)

# Set up OpenAI
openai.api_key = "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"  # Replace with your OpenAI API key
 
# Define a function to handle incoming messages


def handle_incoming_message(from_number, body):
    # Use GPT-3 to generate a response to the message
    response = openai_client.engine.create_completion(
        model="gpt-3.5-turbo", prompt=body, temperature=0.7).text

    # Check if the message is a question
    if body.endswith("?"):
        # Use GPT-3 to generate an answer to the question
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a chatbot."},
            {"role": "user", "content": body},
        ],)
    elif "inquiry" in body.lower() or "complaint" in body.lower():
        # Handle customer inquiries and complaints
        response = "We apologize for any inconvenience you may have experienced. Please send us more details about your inquiry or complaint, and we will do our best to resolve the issue as soon as possible."
    elif "recommendation" in body.lower():
        # Provide personalized recommendations
        response = "Based on your past purchases and browsing history, we recommend the following products: [Product A, Product B, Product C]."
    elif "promotional" in body.lower():
        # Send promotional messages
        response = "Thank you for your interest in our products! We are currently running a sale on [Product A, Product B, Product C]. Use promo code ABC123 at checkout to save 20%."
    elif "appointment" in body.lower():
        # Schedule appointments
        response = "We would be happy to schedule an appointment for you. Please let us know the date and time that you prefer, and we will do our best to accommodate your request."
    elif "order" in body.lower():
        # Process orders
        response = "Thank you for your order! Your purchase will be shipped to you within 3-5 business days. If you have any questions about your order, please don't hesitate to ask."
    elif "reminder" in body.lower():
        # Send reminders
        response = "We'll be happy to set a reminder for you. Please let us know the date and time you would like to be reminded, and the message you would like us to send you."
    elif "support" in body.lower():
        # Provide support
        response = "We are here to help! Please let us know how we can assist you, and we will do our best to resolve any issues you may be experiencing."
    elif "feedback" in body.lower():
        # Gathering feedback
        response = "We value your feedback and appreciate you taking the time to share it with us. Your thoughts and opinions help us to improve our products and services."
    elif "information" in body.lower():
        # Providing information
        response = "We would be happy to provide you with more information about our products and services. Please let us know what specific information you are looking for, and we will do our best to help."
    else:
        # Use GPT-3 to generate a general response
       response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a chatbot."},
            {"role": "user", "content": body},
        ],)

    # Send the response back to the user via SMS
    message = twilio_client.messages.create(
        to=from_number, from_=twilio_phone_number, body=response)

# Set up a Flask route to listen for incoming messages


@app.route("/sms", methods=["POST"])
def sms_reply():
    # Get the incoming message details
    from_number = request.form["From"]
    body = request.form["Body"]

    # Handle the incoming message
    handle_incoming_message(from_number, body)

    # Return an empty TwiML response
    return str(twilio.twiml.Response())

