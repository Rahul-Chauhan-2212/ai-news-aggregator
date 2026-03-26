import smtplib
from email.mime.text import MIMEText
from app.config.settings import EMAIL, EMAIL_APP_PASSWORD
from app.database.repository import get_summarized

def send_email():
    articles = get_summarized()

    body = "🧠 AI News\n\n"
    for a in articles:
        body += f"{a.title}\n{a.summary}\n{a.url}\n\n"

    msg = MIMEText(body)
    msg["Subject"] = "Daily AI News"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.starttls()
        s.login(EMAIL, EMAIL_APP_PASSWORD)
        s.send_message(msg)