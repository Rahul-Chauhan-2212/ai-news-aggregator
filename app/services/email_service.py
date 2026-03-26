import smtplib
from email.mime.text import MIMEText
from app.config.settings import EMAIL, EMAIL_APP_PASSWORD
from app.database.repository import (
    get_active_subscribers,
    get_summarized,
    update_last_email_sent,
)


def send_email_to_users():
    subscribers = get_active_subscribers()
    articles = get_summarized()

    if not articles:
        print("No summarized articles available, skipping email.")
        return

    sent_count = 0
    for user in subscribers:
        try:
            send_email_to_user(user.email, articles)
            sent_count += 1
        except Exception as e:
            print(f"Failed to send to {user.email}: {e}")

    print(f"Newsletter sent to {sent_count} subscribers")


def send_email_to_user(user_email, articles=None):
    """Send newsletter to a specific user"""
    if articles is None:
        articles = get_summarized()

    body = "🧠 AI News\n\n"
    for a in articles:
        body += f"{a.title}\n{a.summary}\n{a.url}\n\n"

    msg = MIMEText(body)
    msg["Subject"] = "Daily AI News"
    msg["From"] = EMAIL
    msg["To"] = user_email

    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.starttls()
        s.login(EMAIL, EMAIL_APP_PASSWORD)
        s.send_message(msg)
    update_last_email_sent(user_email)
