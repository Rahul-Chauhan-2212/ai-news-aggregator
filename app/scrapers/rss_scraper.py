import feedparser
from app.config.sources import RSS_FEEDS
from app.utils.date_utils import parse_rss_date, within_last_n_days

class RSSScraper:
    def fetch(self, days_back=6, max_per_feed=20):
        articles = []

        for url in RSS_FEEDS:
            feed = feedparser.parse(url)

            for entry in feed.entries[:max_per_feed]:
                published_date = parse_rss_date(entry, "published")
                updated_date = parse_rss_date(entry, "updated")

                if not published_date and updated_date:
                    published_date = updated_date

                if not within_last_n_days(published_date, days_back):
                    continue

                articles.append({
                    "title": entry.title,
                    "url": entry.link,
                    "content": entry.get("summary", ""),
                    "source": "rss",
                    "published_date": published_date,
                    "updated_date": updated_date
                })

        return articles