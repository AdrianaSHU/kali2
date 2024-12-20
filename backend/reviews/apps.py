from django.apps import AppConfig

app = 'reviews'

class ReviewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews'

class ReviewsConfig(AppConfig):
    name = 'reviews'

    def ready(self):
        import reviews.signals