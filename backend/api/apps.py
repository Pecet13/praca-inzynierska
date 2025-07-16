from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        from apscheduler.schedulers.background import BackgroundScheduler
        from .services import update_rankings

        # Ensure the scheduler is only started once
        if getattr(self, 'scheduler_started', False):
            return

        scheduler = BackgroundScheduler()
        scheduler.add_job(
            update_rankings,
            'interval',
            minutes=5,
            id='update_rankings_job',
            replace_existing=True,
            max_instances=1,
        )
        scheduler.start()
        self.scheduler_started = True
