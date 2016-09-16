"""
This program sends an SMS message to any cell phone
using Gmail's SMTP gateway.
"""

import smtplib

# Establish a secure session with Gmail's
# outgoing SMTP server using your gmail account
server = smtplib.SMTP("smtp.gmail.com", 587)

# Puts the SMTP connection in TLS (Transport Layer Security Mode
# All SMTP commands that follow will be encrypted
server.starttls()

# Login using your Gmail address and password
server.login("gmail_address", "gmail_address_password")

"""
Use the SMS gateway provided by your mobile carrier:

AT&T:        number@mms.att.net
T-Mobile:    number@tmomail.net
Verizon:     number@vtext.com
Sprint:      number@page.nextel.com

Replace the number prefix with your phone number.
"""

"""
Message details

sender can be anything, but the text message will always show as
being send from your Gmail address.

receiver must be in the format of the SMS gateway provided by your
mobile carrier above. Example: 5555555555@vtext.com

body is the actual contents of the message
"""
sender = "sender_name"
receiver = "phone_number@mobile_carrier_sms_gateway"
body = "Message content goes here"

# Message creation
# This message format must be used because message headers must be included
# A subject header can also be used after the To header
message = ("From: %s\r\n" % sender
           + "To: %s\r\n" % receiver
           + "\r\n"
           + body)

# Send a text message through the SMS gateway of the destination number
server.sendmail(sender, receiver, message)
