from app.database.connection import SessionLocal
from app.database.models import Article, User
from datetime import datetime


def save_article(data):
    db = SessionLocal()

    if db.query(Article).filter_by(url=data["url"]).first():
        db.close()
        return

    article = Article(**data)
    db.add(article)
    db.commit()
    db.close()


def get_unsummarized():
    db = SessionLocal()
    res = db.query(Article).filter(Article.summary == None).all()
    db.close()
    return res


def get_summarized():
    db = SessionLocal()
    res = db.query(Article).filter(Article.summary != None).all()
    db.close()
    return res


def update_summary(article_id, summary):
    db = SessionLocal()
    article = db.get(Article, article_id)
    article.summary = summary
    db.commit()
    db.close()


# User management functions
def subscribe_user(email):
    db = SessionLocal()
    user = db.query(User).filter_by(email=email).first()
    if user:
        user.is_active = True
        db.commit()
    else:
        user = User(email=email)
        db.add(user)
        db.commit()
    db.close()
    return user


def unsubscribe_user(email):
    db = SessionLocal()
    user = db.query(User).filter_by(email=email).first()
    if user:
        user.is_active = False
        db.commit()
    db.close()


def get_active_subscribers():
    db = SessionLocal()
    res = db.query(User).filter(User.is_active).all()
    db.close()
    return res


def update_last_email_sent(email):
    db = SessionLocal()
    user = db.query(User).filter_by(email=email).first()
    user.last_email_sent = datetime.utcnow()
    db.commit()
    db.close()
