from django.db import models


class User(models.Model):
    use_in_migrations = True
    user_email = models.TextField()
    password = models.CharField(max_length=10)
    user_name = models.TextField()
    phone = models.TextField(null=True)
    birth = models.TextField(null=True)
    address = models.TextField(null=True)
    job = models.TextField(null=True)
    user_interests = models.TextField(null=True)
    token = models.TextField(null=True)

    def __str__(self):
        return f'{self.pk}'

    class Meta:
        db_table = "users"

