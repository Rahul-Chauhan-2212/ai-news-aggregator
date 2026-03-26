from fastapi import FastAPI, Form, Request
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database.repository import (
    get_active_subscribers,
    get_summarized,
    subscribe_user,
    unsubscribe_user,
)
from app.database.tables_create import init_db
from app.jobs.daily_pipeline import run_pipeline
from app.services.email_service import send_email_to_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    init_db()
    print("DB initialized")

    print("Running startup tasks...")
    run_pipeline()  # Run the daily pipeline on startup to ensure we have data and send emails if needed

    yield

    # shutdown (optional)
    print("App shutting down")


app = FastAPI(title="AI News Aggregator", lifespan=lifespan)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Display the latest AI news"""
    try:
        articles = get_summarized()
        return templates.TemplateResponse(request, "index.html", {"articles": articles})
    except Exception as e:
        import traceback

        return templates.TemplateResponse(
            request,
            "error.html",
            {
                "error": str(e),
                "traceback": traceback.format_exc(),
            },
        )


@app.get("/subscribe", response_class=HTMLResponse)
async def subscribe_form(request: Request):
    """Show subscription form"""
    return templates.TemplateResponse(request, "subscribe.html", {})


@app.post("/subscribe", response_class=HTMLResponse)
async def subscribe(request: Request, email: str = Form(...)):
    try:
        subscribe_user(email)

        return templates.TemplateResponse(
            request,
            "subscribe.html",
            {"message": f"Successfully subscribed {email}!", "success": True},
        )

    except Exception as e:
        return templates.TemplateResponse(
            request,
            "subscribe.html",
            {"message": str(e), "success": False},
        )


@app.post("/unsubscribe", response_class=HTMLResponse)
async def unsubscribe(request: Request, email: str = Form(...)):
    """Handle email unsubscription"""
    try:
        unsubscribe_user(email)
        return templates.TemplateResponse(
            request,
            "subscribe.html",
            {"message": f"Successfully unsubscribed {email}!", "success": True},
        )
    except Exception as e:
        return templates.TemplateResponse(
            request,
            "s.html",
            {"message": str(e), "success": False},
        )


@app.get("/admin/subscribers")
async def get_subscribers():
    """Get list of active subscribers (for admin)"""
    subscribers = get_active_subscribers()
    return {"subscribers": [user.email for user in subscribers]}


@app.post("/admin/send-newsletter")
async def send_newsletter():
    """Send newsletter to all subscribers"""
    subscribers = get_active_subscribers()
    articles = get_summarized()

    if not articles:
        return {"message": "No summarized articles available"}

    sent_count = 0
    for user in subscribers:
        try:
            send_email_to_user(user.email, articles)
            sent_count += 1
        except Exception as e:
            print(f"Failed to send to {user.email}: {e}")

    return {"message": f"Newsletter sent to {sent_count} subscribers"}


@app.get("/api/news")
async def get_news_api():
    """API endpoint to get news data"""
    articles = get_summarized()
    return {
        "articles": [
            {
                "title": article.title,
                "summary": article.summary,
                "url": article.url,
                "published_date": article.published_date.isoformat()
                if article.published_date
                else None,
                "source": article.source,
            }
            for article in articles
        ]
    }
