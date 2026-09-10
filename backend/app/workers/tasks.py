try:
    from celery import shared_task
except ImportError:
    def shared_task(*args, **kwargs):
        def decorator(fn):
            return fn
        return decorator

from .pipeline import run_extraction_and_analysis

@shared_task(name="process_content_task", bind=True)
def process_content_task(self, source_id: str):
    run_extraction_and_analysis(source_id)
    return {"status": "completed", "source_id": source_id}
