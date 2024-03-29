import smtplib
import ssl
import traceback

def send_email(subject, body):
    """Send email via SMTP"""

    smtp_user = ''
    smtp_password = ''
    sender = ''
    receiver = ''

    message = f'Subject: {subject}\n\n{body}'
    print(f'sending email: {message}')

    try:
        # Create a secure SSL context
        ssl_context = ssl.create_default_context()
        with smtplib.SMTP_SSL('email-smtp.us-east-1.amazonaws.com', 465, context=ssl_context) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(sender, receiver, message)
    except Exception:
        traceback.print_exc()
        return False

    return True
