import imaplib
import email
import smtplib
import time
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from ollama import Client

# Email account credentials
EMAIL = '<email address>'
PASSWORD = '<google app password>'

# IMAP server settings for Gmail
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993

# SMTP server settings for Gmail
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# Predefined list of email addresses to process
email_list = [
    "<phone1>",
    "<phone2>",
    "<etc>
]

def read_emails():
    while True:
        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL, PASSWORD)
        mail.select('inbox')

        # Search for unread emails
        result, data = mail.search(None, 'UNSEEN')
        email_ids = data[0].split()

        for email_id in email_ids:
            # Fetch the email
            result, data = mail.fetch(email_id, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Check if the email is from a predefined address
            sender_email = msg['From']
            if sender_email in email_list:
                # Process the email contents
                # Example: print the subject and body
                print('Subject:', msg['Subject'])
                print('From:', sender_email)
                print('Body:', msg.get_payload())

                # Respond to the email
                response = process_email(msg)
                send_email(sender_email, '', response)

                # Mark the email as read
                mail.store(email_id, '+FLAGS', '\\Seen')
            else:
                print("Bad sender " + sender_email)

        # Close the connection
        mail.close()
        mail.logout()

        # Wait for 10 seconds before checking for new emails again
        time.sleep(10)

def process_email(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == 'text/plain':
                body += part.get_payload(decode=True).decode('utf-8')
    else:
        body += msg.get_payload(decode=True).decode('utf-8')

    # If body is still empty, try fetching from the email body
    if not body:
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == 'text/html':
                    html_content = part.get_payload(decode=True).decode('utf-8')
                    # Parse the HTML content to extract text within <td> tags
                    soup = BeautifulSoup(html_content, 'html.parser')
                    td_content = soup.find('td').get_text()
                    # Append the extracted text to the body
                    body += td_content

    # Initialize the Ollama client outside the loop
    client = Client(host='http://localhost:11434')
    print("Body: " + body)
    # Process the entire email body
    response = client.chat(model='llama2', messages=[
        {
            'role': 'user',
            'content': body,
            'stream': False
        },
    ])

    # Extract the response content
    response_content = response['message']['content']

    print(response_content)

    return response_content

def send_email(to, subject, response_content):
    # Connect to the SMTP server
    smtp_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp_server.starttls()
    smtp_server.login(EMAIL, PASSWORD)

    # Compose the email
    msg = MIMEText(response_content)
    msg['From'] = EMAIL
    msg['To'] = to
    msg['Subject'] = subject

    # Send the email
    smtp_server.send_message(msg)

    # Close the connection
    smtp_server.quit()

if __name__ == '__main__':
    read_emails()
