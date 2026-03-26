from app.database.repository import get_unsummarized, update_summary
from app.agents.summarizer_agent import SummarizerAgent
from app.ai.factory import get_ai_provider

def run_processing():
    agent = SummarizerAgent(get_ai_provider())
    articles = get_unsummarized()

    for a in articles:
        summary = agent.run(a.content)
        update_summary(a.id, summary)

    print("Processing complete")