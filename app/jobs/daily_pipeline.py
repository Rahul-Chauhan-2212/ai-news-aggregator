from app.services.ingestion_service import run_ingestion
from app.services.processing_service import run_processing
from app.services.email_service import send_email

def run_pipeline():
    run_ingestion()
    run_processing()
    send_email()