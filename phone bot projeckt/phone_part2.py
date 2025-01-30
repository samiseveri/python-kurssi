from twilio.rest import Client
account_sid = 'AC49e54d565b659a7a8ccbfcff5f2d12be'
auth_token = '4f4decda804995eec61d3074deb697a3'
client = Client(account_sid, auth_token)
message = client.messages.create(
  from_='+18154738194',
  body='message XD',
  to='+358440101160'
)
print(message.sid)