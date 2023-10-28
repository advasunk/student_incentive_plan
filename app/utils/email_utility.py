import smtplib, ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "incenti.help@gmail.com"  # Enter your address
receiver_email = "sunkarsr@gmail.com"  # Enter receiver address
# password = "xatsif-1nyvni-haHzin"
password = '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'
message = """\
Subject: Hi there

This message is sent from Python.
"""

"""
    https://www.google.com/search?q=python+gmail+api+to+send+mail+using+client+id+and+secret&oq=python+gmail+api+to+send+mail+using+client+id+and+se&gs_lcrp=EgZjaHJvbWUqBwgBECEYoAEyBggAEEUYOTIHCAEQIRigATIHCAIQIRigATIHCAMQIRirAtIBCTExNjM3ajBqNKgCALACAA&sourceid=chrome&ie=UTF-8
    
    https://developers.google.com/gmail/api/quickstart/python
    
"""


context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
