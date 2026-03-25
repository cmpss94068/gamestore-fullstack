from django.db import models
from django.contrib.auth.models import User
from gameprofile.models import profile 
# Create your models here.

class order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    games = models.ManyToManyField(profile, through='orderItem')
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'Order {self.pk}'

    def get_total_price(self):
        return sum(item.get_item_price() for item in self.order_items.all())

class orderItem(models.Model):
    order = models.ForeignKey(order, related_name='order_items', on_delete=models.CASCADE)
    game = models.ForeignKey(profile, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.game.game_name}'

    def get_item_price(self):
        return self.quantity * self.game.game_price