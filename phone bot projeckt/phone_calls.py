from twilio.rest import Client


# in this part you have to replace account_sid
# auth_token, twilio_number, recipient_number with your actual credential

account_sid = 'AC49e54d565b659a7a8ccbfcff5f2d12be'
auth_token = '4f4decda804995eec61d3074deb697a3'
twilio_number = '+3580440101160'
recipient_number = '+3580440101160'

# Create Twilio client
client = Client(account_sid, auth_token)

# Send SMS
# in body part you have to write your message
message = client.messages.create(
    body='This is a new message',
    from_=twilio_number,
    to=recipient_number
)

print(f"Message sent with SID: {message.sid}")

