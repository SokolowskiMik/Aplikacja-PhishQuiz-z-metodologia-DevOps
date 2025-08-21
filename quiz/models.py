from django.db import models

class QuizQuestion(models.Model):
    """
    Model to store a single phishing quiz question.
    It consists of one real URL and two phishing URLs.
    """
    real_url = models.URLField(max_length=500, help_text="The legitimate URL.")
    phishing_url_1 = models.URLField(max_length=500, help_text="A phishing URL.")
    phishing_url_2 = models.URLField(max_length=500, help_text="Another phishing URL.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question {self.id}: {self.real_url}"