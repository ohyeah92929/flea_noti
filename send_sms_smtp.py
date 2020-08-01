import smtplib
from email.message import EmailMessage

def send_sms_smtp(email, pw, phone_no, gate_way, content="content", smtp="smtp.gmail.com", port=587):
  sms_gateway = phone_no+"@"+gate_way #'5127015477@vtext.com'

  # This will start our email server
  server = smtplib.SMTP(smtp,port)
  # Starting the server
  server.starttls()
  # Now we need to login
  server.login(email,pw)

  msg = EmailMessage()
  #msg['Subject'] = content
  msg.set_content(content)
  msg['From'] = email
  msg['To'] = sms_gateway
  msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'
  server.send_message(msg)

# lastly quit the server
  server.quit()

