# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


def send_sms(to, body):
    print(to, body)
    account_sid = os.environ['TWILIO_ACCOUNT_SID'] = 'AC1d10ba68e6c55298bafe90feec8f326e'
    auth_token = os.environ['TWILIO_AUTH_TOKEN'] = 'c9938e98d355d0639916f22e94af81b8'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body='your verification code is ' + str(
            body) + ' , please do not share with others, the verification code will expire after 60 seconds.',
        from_='+13369999214',
        to=to
    )

    if message.sid:
        return True
    else:
        return False
