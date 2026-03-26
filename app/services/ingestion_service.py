from app.scrapers.rss_scraper import RSSScraper
from app.database.repository import save_article


def run_ingestion():
    scraper = RSSScraper()
    articles = scraper.fetch()

    for a in articles:
        save_article(a)

    print("Ingestion complete")
