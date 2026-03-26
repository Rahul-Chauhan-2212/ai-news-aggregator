from app.database.connection import SessionLocal
from app.database.models import Article

def save_article(data):
    db = SessionLocal()

    if db.query(Article).filter_by(url=data["url"]).first():
        db.close()
        return

    article = Article(**data)  # Now includes updated_at (auto-handled)
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
    article.summary = summary  # This will trigger updated_at auto-update
    db.commit()
    db.close()