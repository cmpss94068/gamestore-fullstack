from django.db import models

# Create your models here.
class profile(models.Model):
    game_name = models.CharField(max_length=100)
    game_img = models.URLField()
    game_url = models.URLField(unique=True)
    game_rating = models.DecimalField(max_digits=10, decimal_places=2)
    game_price = models.DecimalField(max_digits=10, decimal_places=0)
    platform = models.ManyToManyField('platform', related_name='platform')
    game_date = models.DateField()
    game_publisher = models.CharField(max_length=100)
    category = models.ManyToManyField('category', related_name='category')

    def __str__(self):
        return self.game_name

class platform(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name