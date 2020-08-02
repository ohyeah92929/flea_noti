import smtplib 
from email.message import EmailMessage

def send_sms_smtp(email, pw, phone_addr, content="content", smtp="smtp.gmail.com", port=587):
  # Create email message
  msg = EmailMessage()
  msg.set_content(content)
  msg['From'] = email
  msg['To'] = phone_addr
  #msg['Subject'] = "title"
  #msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'
  
  # Send the message
  server = smtplib.SMTP(smtp,port)  # This will start our email server
  server.starttls()  # Starting the server
  server.login(email,pw)
  server.send_message(msg)
  server.quit()
